"""
On-disk persistence for ThreatChain prototype.

Each running node has its own data directory (so you can launch several nodes on
one machine for the demo). A node's directory holds:

  data/<node_name>/chain.json     — the blockchain itself
  data/<node_name>/orgs.json      — registry of every org this node has seen
  data/<node_name>/peers.json     — list of peer node URLs

For simplicity and demo-ability we use plain JSON files, no SQLite.
"""

from __future__ import annotations

import json
import os
import threading
import time
from pathlib import Path

from blockchain import Blockchain


_LOCK = threading.RLock()


class NodeStore:
    def __init__(self, root: Path, blockchain: Blockchain):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.chain_path = self.root / "chain.json"
        self.orgs_path = self.root / "orgs.json"
        self.peers_path = self.root / "peers.json"
        self.blockchain = blockchain

    # ── chain ──

    def save_chain(self) -> None:
        with _LOCK:
            self.chain_path.write_text(json.dumps(self.blockchain.to_dict(), indent=2))

    def load_chain(self) -> None:
        if not self.chain_path.exists():
            return
        with _LOCK:
            self.blockchain.load_dict(json.loads(self.chain_path.read_text()))

    # ── orgs ──

    def load_orgs(self) -> dict[str, dict]:
        if not self.orgs_path.exists():
            return {}
        return json.loads(self.orgs_path.read_text())

    def save_orgs(self, orgs: dict[str, dict]) -> None:
        with _LOCK:
            self.orgs_path.write_text(json.dumps(orgs, indent=2))

    def register_org(self, name: str, sector: str, public_pem: str, private_pem: str | None) -> dict:
        """Add an org to the local registry. `private_pem` may be None on remote nodes
        that only learned about the org via gossip — they need the public key to
        verify signatures, but they should never see the private key."""
        orgs = self.load_orgs()
        from crypto_utils import fingerprint
        fp = fingerprint(public_pem)
        orgs[fp] = {
            "name": name,
            "sector": sector,
            "public_pem": public_pem,
            "private_pem": private_pem,
            "fingerprint": fp,
            "registered_at": time.time(),
        }
        self.save_orgs(orgs)
        return orgs[fp]

    def get_org(self, fp: str) -> dict | None:
        return self.load_orgs().get(fp)

    # ── peers ──

    def load_peers(self) -> list[str]:
        if not self.peers_path.exists():
            return []
        return json.loads(self.peers_path.read_text())

    def save_peers(self, peers: list[str]) -> None:
        with _LOCK:
            self.peers_path.write_text(json.dumps(sorted(set(peers)), indent=2))

    def add_peer(self, url: str) -> list[str]:
        url = url.rstrip("/")
        peers = self.load_peers()
        if url not in peers:
            peers.append(url)
            self.save_peers(peers)
        return self.load_peers()

    def remove_peer(self, url: str) -> list[str]:
        url = url.rstrip("/")
        peers = [p for p in self.load_peers() if p != url]
        self.save_peers(peers)
        return peers


def data_dir_for(node_name: str) -> Path:
    here = Path(__file__).parent
    return here / "data" / node_name
