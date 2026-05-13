# ThreatChain — Prototype

A working prototype of a **decentralized threat-intelligence platform** for the
graduation project, built with Python + Flask + a custom blockchain.

Every organization (bank, CERT, ISP, hospital…) registers on the network with an
RSA keypair. They can then submit signed threat intelligence (malware indicators,
phishing URLs, malicious IPs…). Every submission is sealed into a block via
proof-of-work and gossiped to all peer nodes. Tampering is impossible because
each block's hash depends on the previous block's hash, and every other node
will reject an invalid chain.

---

## What's a "real" blockchain here?

Everything you'd expect:

| Feature | How it's done in this prototype |
| --- | --- |
| Immutable ledger | SHA-256 hash chain — modifying any past block invalidates every block after it. |
| Consensus | Proof-of-work (4 leading zeros). Adjustable in `blockchain.py`. |
| Decentralization | Multiple nodes, each holding a full copy. Longest-valid-chain rule. |
| Identity | 2048-bit RSA keypair per organization. |
| Authenticity | Every threat is signed (RSA-PSS-SHA256) and verified on every node. |
| Persistence | Each node persists its chain to JSON on disk. |

It's a real, demo-able blockchain you built yourself — not a wrapper over Ethereum.

---

## Setup (Windows)

```bat
cd prototype
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

(Uses Python 3.10+.)

---

## Run

### Option A — single node

```bat
python app.py --node alice --port 5000
```

Open http://127.0.0.1:5000 → register an org → submit a threat → see it sealed
into a block.

### Option B — three-node demo network (recommended for the presentation)

```bat
run_demo.bat
```

This opens three terminal windows:

| Node  | URL                       | Suggested role              |
| ----- | ------------------------- | --------------------------- |
| alice | http://127.0.0.1:5000     | National CERT               |
| bob   | http://127.0.0.1:5001     | Acme Bank                   |
| carol | http://127.0.0.1:5002     | Memorial Hospital           |

On each node, register a different organization, submit a threat, then open the
other nodes — the threat will appear there too (broadcast over P2P), sealed
into the same block, with the signature verified locally.

---

## Walkthrough for the demo / examiner

1. **Open alice (port 5000) and bob (port 5001) side-by-side.**
2. Register *National CERT* on alice and *Acme Bank* on bob.
3. On alice, submit a threat: malware C2 IP `185.220.101.47`, severity `critical`.
   - Watch the flash message: *"Threat sealed in block #N after 0.3s of PoW."*
4. Refresh bob's dashboard — the same threat appears there, broadcast and verified.
5. Open the **Blockchain** tab on either node — show the block list, hashes, nonces,
   and that the chain is marked `● valid`.
6. Open `prototype/data/alice/chain.json` in a text editor and change one byte
   inside a transaction title. Refresh the explorer — chain is now `● invalid`,
   and the next sync from a peer will overwrite the corrupted local copy with the
   valid one. *This proves immutability and consensus.*

---

## Project layout

```
prototype/
├── app.py            Flask node (single entry point)
├── blockchain.py     Block, Blockchain, PoW, validation
├── crypto_utils.py   RSA keypairs, sign, verify
├── p2p.py            Peer gossip and consensus sync
├── storage.py        Per-node JSON persistence
├── templates/        Jinja2 HTML pages
├── static/style.css  Visual style (matches existing mockup)
├── data/<node>/      Auto-created. chain.json + orgs.json + peers.json per node
├── requirements.txt
├── run_node.bat      Launch one node
└── run_demo.bat      Launch three nodes in a network
```

---

## HTTP API (for an examiner who asks)

| Method | Path                       | Purpose                                  |
| ------ | -------------------------- | ---------------------------------------- |
| GET    | `/api/chain`               | Full blockchain (used by peers to sync). |
| GET    | `/api/threats`             | Flat list of threats on the chain.       |
| GET    | `/api/orgs`                | Public registry (no private keys).       |
| GET    | `/api/peers`               | Known peers.                             |
| GET    | `/api/stats`               | Node summary: blocks/threats/orgs/peers. |
| POST   | `/api/threats/receive`     | Receive a gossiped tx from a peer.       |
| POST   | `/api/peers/register`      | Add a peer URL.                          |
| POST   | `/api/sync`                | Trigger consensus sync now.              |

---

## Things you can extend after the demo (if you have time)

- Difficulty adjustment over time (currently fixed at 4 zeros).
- WebSocket push instead of polling refresh on the live feed.
- Reputation score per organization (e.g. how many of its threats were
  confirmed by peers).
- Encrypted private keys at rest (`cryptography.BestAvailableEncryption`).
- Sharing on multiple machines instead of one (set `--host 0.0.0.0` and use the
  LAN IP as the peer URL).
