# ThreatChain 🔗🛡️

**Decentralized Threat Intelligence Sharing on Blockchain**

A graduation project (Cybersecurity, Tafila Technical University) that lets organizations share cyber-threat intelligence on a tamper-proof, custom-built blockchain — no central authority, no single point of failure.

## The Problem

When an organization is attacked, others facing the same threat usually find out too late. Centralized threat-sharing platforms require trusting a middleman, can be censored or taken down, and give no cryptographic proof of **who** reported a threat or **whether the record was altered**.

## The Solution

ThreatChain stores every threat report in a blockchain replicated across independent nodes:

- **Tamper-proof** — each block is sealed with SHA-256 and linked to the previous one; changing any record breaks the chain.
- **Authenticated** — every report is digitally signed (RSA-2048, RSA-PSS-SHA256) by the submitting organization, so impersonation is impossible.
- **Decentralized** — nodes sync over a P2P protocol (longest-valid-chain); there is no central server to compromise.

## Architecture

| Layer | What it does |
|---|---|
| **Web Interface** | Flask web app — dashboard, threat submission, block explorer, network view |
| **P2P Network** | Peer registration, chain exchange, transaction gossip over HTTP |
| **Cryptographic Identity** | RSA-2048 keypairs per organization, RSA-PSS signatures, key fingerprints |
| **Blockchain Core** | SHA-256 hash chain + Proof-of-Work consensus (difficulty 4) |
| **Persistence** | Per-node JSON storage of chain, keys, and pending transactions |

### How a threat report flows

1. An analyst submits a threat (IOCs, severity, mitigation) through the web UI.
2. The report is serialized to **canonical JSON** (`sort_keys=True`) and signed with the org's private key.
3. The signed transaction is gossiped to peers and mined into a block (Proof-of-Work).
4. Every node independently verifies: block hash, difficulty, chain linkage, and signature — then appends it to its local chain.
5. Any organization can now read the threat, verify its origin, and export a PDF report with full cryptographic provenance.

## Tech Stack

- **Python 3.12** · **Flask** — web app & HTTP P2P
- **cryptography** (PyCA / OpenSSL) — RSA key generation, signing, verification
- **hashlib** — SHA-256 block hashing & Proof-of-Work
- **ReportLab** — PDF threat reports with provenance (block hash, tx ID, signature)

## Quick Start

```bash
cd prototype
pip install -r requirements.txt
```

Run a 3-node demo network (Windows):

```bash
run_demo.bat
```

Or start a single node:

```bash
python app.py --node alice --port 5000
```

Then open `http://127.0.0.1:5000`, register an organization (a keypair is generated for you), and submit a threat.

## Project Structure

```
prototype/
├── app.py           # Flask routes & web UI
├── blockchain.py    # Block, chain, Proof-of-Work, validation
├── crypto_utils.py  # RSA keys, canonical JSON, sign/verify
├── p2p.py           # Peer sync & transaction gossip
├── storage.py       # Per-node persistence
├── mitigations.py   # Standard mitigation playbooks
├── pdf_report.py    # PDF threat-report generator
├── templates/       # Jinja2 HTML pages
└── static/          # CSS (light theme)
```

## Author

**Abdullah Moneer** — Cybersecurity, Tafila Technical University

## License

MIT — see [LICENSE](LICENSE).
