"""
ThreatChain — Flask node.

Run a single node:
    python app.py --node alice --port 5000

Run a second node and have it sync from the first:
    python app.py --node bob   --port 5001 --peer http://127.0.0.1:5000

Each node has its own data folder, its own chain, and its own org keypairs.
Nodes synchronize via the longest-valid-chain rule.
"""

from __future__ import annotations

import argparse
import secrets
import threading
import time
from pathlib import Path

from flask import (
    Flask, jsonify, redirect, render_template, request, session, url_for, abort, flash,
    Response,
)

from blockchain import Blockchain, make_threat_tx
from crypto_utils import fingerprint, generate_keypair
from mitigations import MITIGATIONS, get_playbook
from pdf_report import build_threat_report
from storage import NodeStore, data_dir_for
import p2p


# ─────────────────────────── factory ───────────────────────────

def create_app(node_name: str, public_url: str) -> Flask:
    app = Flask(__name__)
    app.secret_key = secrets.token_hex(16)
    app.config["NODE_NAME"] = node_name
    app.config["PUBLIC_URL"] = public_url.rstrip("/")

    @app.template_filter("timestamp")
    def _ts_filter(value):
        try:
            return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(value)))
        except (ValueError, TypeError, OSError):
            return "—"

    @app.context_processor
    def _inject_globals():
        # makes MITIGATIONS and get_playbook available in every template
        return {"MITIGATIONS": MITIGATIONS, "get_playbook": get_playbook}

    blockchain = Blockchain()
    store = NodeStore(data_dir_for(node_name), blockchain)
    store.load_chain()

    app.config["BLOCKCHAIN"] = blockchain
    app.config["STORE"] = store

    # ── helpers ──

    def current_org():
        fp = session.get("org_fp")
        return store.get_org(fp) if fp else None

    def merge_orgs(remote_orgs: dict):
        local = store.load_orgs()
        for fp, info in remote_orgs.items():
            if fp not in local:
                local[fp] = {**info, "private_pem": None}
        store.save_orgs(local)

    # ── pages ──

    @app.route("/")
    def landing():
        return render_template("landing.html",
                               node=node_name,
                               public_url=public_url,
                               chain_len=len(blockchain.chain),
                               threat_count=len(blockchain.all_threats()),
                               org_count=len(store.load_orgs()))

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            sector = request.form.get("sector", "").strip()
            if not name or not sector:
                flash("Please fill in all fields.", "error")
                return redirect(url_for("register"))
            private_pem, public_pem = generate_keypair()
            org = store.register_org(name, sector, public_pem, private_pem)
            session["org_fp"] = org["fingerprint"]
            flash(f"Registered '{name}'. You are now logged in as this organization.", "ok")
            return redirect(url_for("dashboard"))
        return render_template("register.html", node=node_name)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        orgs = store.load_orgs()
        own = {fp: o for fp, o in orgs.items() if o.get("private_pem")}
        if request.method == "POST":
            fp = request.form.get("org_fp")
            if fp not in own:
                flash("Unknown organization for this node.", "error")
                return redirect(url_for("login"))
            session["org_fp"] = fp
            return redirect(url_for("dashboard"))
        return render_template("login.html", node=node_name, orgs=own)

    @app.route("/logout")
    def logout():
        session.pop("org_fp", None)
        return redirect(url_for("landing"))

    @app.route("/dashboard")
    def dashboard():
        org = current_org()
        if not org:
            return redirect(url_for("login"))
        return render_template("dashboard.html",
                               node=node_name,
                               org=org,
                               chain_len=len(blockchain.chain),
                               pending_count=len(blockchain.pending),
                               threats=blockchain.all_threats()[:50],
                               peer_count=len(store.load_peers()))

    @app.route("/dashboard/submit", methods=["GET", "POST"])
    def submit_threat():
        org = current_org()
        if not org:
            return redirect(url_for("login"))
        if request.method == "POST":
            iocs = [s for s in request.form.get("iocs", "").splitlines() if s.strip()]
            github_links = [s for s in request.form.get("github_links", "").splitlines() if s.strip()]
            tx = make_threat_tx(
                submitter_pub=org["public_pem"],
                submitter_name=org["name"],
                threat_type=request.form.get("threat_type", "other"),
                threat_type_custom=request.form.get("threat_type_custom", ""),
                severity=request.form.get("severity", "medium"),
                title=request.form.get("title", ""),
                description=request.form.get("description", ""),
                iocs=iocs,
                mitigation=request.form.get("mitigation", ""),
                github_links=github_links,
                private_pem=org["private_pem"],
            )
            if not blockchain.add_transaction(tx):
                flash("Transaction rejected (invalid signature or duplicate).", "error")
                return redirect(url_for("submit_threat"))

            t0 = time.time()
            block = blockchain.mine_pending()
            mined_in = time.time() - t0
            store.save_chain()

            peers = store.load_peers()
            if peers:
                p2p.broadcast_tx(peers, tx)

            flash(f"Threat sealed in block #{block.index} after {mined_in:.2f}s of PoW.", "ok")
            return redirect(url_for("dashboard"))

        return render_template("submit.html", node=node_name, org=org)

    @app.route("/dashboard/explorer")
    def explorer():
        org = current_org()
        if not org:
            return redirect(url_for("login"))
        blocks = [b.to_dict() for b in reversed(blockchain.chain)]
        return render_template("explorer.html",
                               node=node_name, org=org, blocks=blocks,
                               valid=blockchain.is_valid())

    @app.route("/dashboard/network", methods=["GET", "POST"])
    def network():
        org = current_org()
        if not org:
            return redirect(url_for("login"))
        if request.method == "POST":
            action = request.form.get("action")
            url = request.form.get("peer_url", "").strip().rstrip("/")
            if action == "add" and url and url != public_url:
                store.add_peer(url)
                p2p.announce_to_peer(url, public_url)
                flash(f"Peer added: {url}", "ok")
            elif action == "remove" and url:
                store.remove_peer(url)
                flash(f"Peer removed: {url}", "ok")
            elif action == "sync":
                replaced, reached = p2p.resolve_consensus(blockchain, store.load_peers(), merge_orgs)
                store.save_chain()
                msg = f"Reached {reached} peer(s). "
                msg += "Adopted a longer chain." if replaced else "Local chain already longest."
                flash(msg, "ok")
            return redirect(url_for("network"))
        return render_template("network.html", node=node_name, org=org,
                               peers=store.load_peers(), public_url=public_url)

    @app.route("/threats/<threat_id>/report.pdf")
    def threat_report(threat_id: str):
        """Find the threat by id and stream a per-threat PDF report.
        Public: no login required so PDF links can be shared off-platform."""
        for block in blockchain.chain:
            for tx in block.transactions:
                if tx.get("id") == threat_id:
                    playbook = get_playbook(tx.get("threat_type", "other"))
                    pdf_bytes = build_threat_report(tx, block.index, block.hash, playbook)
                    title = (tx.get("title") or "threat").lower()
                    safe = "".join(c if c.isalnum() else "_" for c in title)[:40]
                    fname = f"threatchain_{safe}_{threat_id[:8]}.pdf"
                    return Response(
                        pdf_bytes,
                        mimetype="application/pdf",
                        headers={
                            "Content-Disposition": f'inline; filename="{fname}"',
                            "Content-Length": str(len(pdf_bytes)),
                        },
                    )
        abort(404)

    @app.route("/dashboard/search")
    def search():
        org = current_org()
        if not org:
            return redirect(url_for("login"))
        q = request.args.get("q", "").strip()
        results = blockchain.search(q) if q else []
        return render_template("search.html", node=node_name, org=org, q=q, results=results)

    # ─────────────────────────── API ───────────────────────────

    @app.get("/api/chain")
    def api_chain():
        return jsonify({
            "node": node_name,
            "length": len(blockchain.chain),
            "chain": [b.to_dict() for b in blockchain.chain],
            "valid": blockchain.is_valid(),
        })

    @app.get("/api/threats")
    def api_threats():
        return jsonify({"threats": blockchain.all_threats()})

    @app.get("/api/stats")
    def api_stats():
        return jsonify({
            "node": node_name,
            "blocks": len(blockchain.chain),
            "threats": len(blockchain.all_threats()),
            "orgs": len(store.load_orgs()),
            "peers": len(store.load_peers()),
            "pending": len(blockchain.pending),
        })

    @app.get("/api/orgs")
    def api_orgs():
        # only expose public material — never leak private_pem
        out = {}
        for fp, o in store.load_orgs().items():
            out[fp] = {k: v for k, v in o.items() if k != "private_pem"}
        return jsonify({"orgs": out})

    @app.post("/api/threats/receive")
    def api_threat_receive():
        tx = request.get_json(silent=True) or {}
        if blockchain.add_transaction(tx):
            blockchain.mine_pending()
            store.save_chain()
            return jsonify({"ok": True})
        return jsonify({"ok": False, "reason": "invalid or duplicate"}), 400

    @app.post("/api/peers/register")
    def api_peers_register():
        body = request.get_json(silent=True) or {}
        url = (body.get("url") or "").rstrip("/")
        if not url:
            return jsonify({"ok": False}), 400
        peers = store.add_peer(url)
        return jsonify({"ok": True, "peers": peers})

    @app.get("/api/peers")
    def api_peers():
        return jsonify({"peers": store.load_peers()})

    @app.post("/api/sync")
    def api_sync():
        replaced, reached = p2p.resolve_consensus(blockchain, store.load_peers(), merge_orgs)
        if replaced:
            store.save_chain()
        return jsonify({"replaced": replaced, "peers_reached": reached, "length": len(blockchain.chain)})

    return app


# ─────────────────────────── entrypoint ───────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--node", default="alice", help="Unique node name (data folder)")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--peer", action="append", default=[],
                        help="URL of a peer node to connect to (can repeat)")
    args = parser.parse_args()

    public_url = f"http://{args.host}:{args.port}"
    app = create_app(args.node, public_url)

    # connect to peers (and ask them to add us back) on startup
    store: NodeStore = app.config["STORE"]
    for peer in args.peer:
        store.add_peer(peer.rstrip("/"))

    def announce():
        time.sleep(0.5)
        for peer in store.load_peers():
            p2p.announce_to_peer(peer, public_url)
        # try to fetch a longer chain right away
        from blockchain import Blockchain  # noqa: F401
        bc = app.config["BLOCKCHAIN"]
        def merge_orgs(remote_orgs):
            local = store.load_orgs()
            for fp, info in remote_orgs.items():
                if fp not in local:
                    local[fp] = {**info, "private_pem": None}
            store.save_orgs(local)
        p2p.resolve_consensus(bc, store.load_peers(), merge_orgs)
        store.save_chain()

    threading.Thread(target=announce, daemon=True).start()

    print(f"\n  ThreatChain node '{args.node}' listening on {public_url}")
    print(f"  Data dir: {data_dir_for(args.node)}")
    print(f"  Peers   : {store.load_peers() or '(none yet)'}\n")
    app.run(host=args.host, port=args.port, debug=False, use_reloader=False)


if __name__ == "__main__":
    main()
