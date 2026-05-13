"""
ThreatChain — custom blockchain core.

A `Block` chains threat-intelligence transactions together. Each block:
  - references the previous block's hash (tamper-evidence)
  - is sealed by proof-of-work (a nonce that drives the hash below a target)
  - contains a list of signed threat transactions

A `Blockchain` enforces:
  - hash continuity            (block.previous_hash == prev.hash)
  - proof-of-work              (block.hash starts with `difficulty` zeros)
  - hash integrity             (recomputed hash == stored hash)
  - signature validity         (each tx signature verifies against the submitter's pubkey)
  - longest-valid-chain rule   (when peers gossip, the longest *valid* chain wins)
"""

from __future__ import annotations

import hashlib
import json
import time
import uuid
from dataclasses import dataclass, field, asdict
from typing import Callable

from crypto_utils import canonical_bytes, sign, verify

DIFFICULTY = 4   # number of leading hex zeros required on a block hash
GENESIS_PREV_HASH = "0" * 64


# ─────────────────────────── transactions ───────────────────────────

def make_threat_tx(
    submitter_pub: str,
    submitter_name: str,
    threat_type: str,
    severity: str,
    title: str,
    description: str,
    iocs: list[str],
    private_pem: str,
    mitigation: str = "",
    github_links: list[str] | None = None,
    threat_type_custom: str = "",
) -> dict:
    """Build and sign a threat transaction.

    New optional fields:
      mitigation         — multi-line defensive steps the submitter recommends.
      github_links       — list of URLs (typically GitHub repos with trained
                           detection / classifier models).
      threat_type_custom — when threat_type == 'other', the human-readable
                           name typed by the submitter.
    """
    payload = {
        "id": uuid.uuid4().hex,
        "submitter_pub": submitter_pub,
        "submitter_name": submitter_name,
        "threat_type": threat_type,
        "threat_type_custom": threat_type_custom.strip(),
        "severity": severity,
        "title": title.strip(),
        "description": description.strip(),
        "iocs": [i.strip() for i in iocs if i.strip()],
        "mitigation": mitigation.strip(),
        "github_links": [u.strip() for u in (github_links or []) if u.strip()],
        "timestamp": time.time(),
    }
    payload["signature"] = sign(private_pem, {k: v for k, v in payload.items() if k != "signature"})
    return payload


def verify_tx(tx: dict) -> bool:
    """Verify a threat transaction's signature."""
    if "signature" not in tx or "submitter_pub" not in tx:
        return False
    body = {k: v for k, v in tx.items() if k != "signature"}
    return verify(tx["submitter_pub"], body, tx["signature"])


# ─────────────────────────── block ───────────────────────────

@dataclass
class Block:
    index: int
    timestamp: float
    transactions: list[dict]
    previous_hash: str
    nonce: int = 0
    hash: str = ""

    def header(self) -> dict:
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
        }

    def compute_hash(self) -> str:
        return hashlib.sha256(canonical_bytes(self.header())).hexdigest()

    def mine(self, difficulty: int = DIFFICULTY, on_progress: Callable[[int], None] | None = None) -> None:
        """Search for a nonce so that compute_hash() starts with `difficulty` zeros."""
        target = "0" * difficulty
        self.nonce = 0
        while True:
            h = self.compute_hash()
            if h.startswith(target):
                self.hash = h
                return
            self.nonce += 1
            if on_progress and self.nonce % 50_000 == 0:
                on_progress(self.nonce)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Block":
        return cls(
            index=d["index"],
            timestamp=d["timestamp"],
            transactions=d["transactions"],
            previous_hash=d["previous_hash"],
            nonce=d["nonce"],
            hash=d["hash"],
        )


# ─────────────────────────── chain ───────────────────────────

class Blockchain:
    def __init__(self, difficulty: int = DIFFICULTY):
        self.difficulty = difficulty
        self.chain: list[Block] = []
        self.pending: list[dict] = []
        if not self.chain:
            self._add_genesis()

    def _add_genesis(self) -> None:
        genesis = Block(index=0, timestamp=0.0, transactions=[], previous_hash=GENESIS_PREV_HASH)
        genesis.mine(self.difficulty)
        self.chain.append(genesis)

    @property
    def last_block(self) -> Block:
        return self.chain[-1]

    # ── transactions ──

    def add_transaction(self, tx: dict) -> bool:
        """Queue a threat tx for the next block. Rejects invalid signatures or duplicates."""
        if not verify_tx(tx):
            return False
        if any(t.get("id") == tx.get("id") for t in self.pending):
            return False
        if any(t.get("id") == tx.get("id") for blk in self.chain for t in blk.transactions):
            return False
        self.pending.append(tx)
        return True

    def mine_pending(self) -> Block | None:
        """Seal pending transactions into a new block via PoW."""
        if not self.pending:
            return None
        block = Block(
            index=self.last_block.index + 1,
            timestamp=time.time(),
            transactions=self.pending,
            previous_hash=self.last_block.hash,
        )
        block.mine(self.difficulty)
        self.chain.append(block)
        self.pending = []
        return block

    # ── validation ──

    def is_valid(self, chain: list[Block] | None = None) -> bool:
        chain = chain if chain is not None else self.chain
        target = "0" * self.difficulty
        for i, block in enumerate(chain):
            if block.compute_hash() != block.hash:
                return False
            if not block.hash.startswith(target):
                return False
            if i == 0:
                if block.previous_hash != GENESIS_PREV_HASH:
                    return False
                continue
            if block.previous_hash != chain[i - 1].hash:
                return False
            for tx in block.transactions:
                if not verify_tx(tx):
                    return False
        return True

    def replace_chain(self, new_chain_dicts: list[dict]) -> bool:
        """Adopt `new_chain_dicts` if it is longer AND valid. Returns True if replaced."""
        new_chain = [Block.from_dict(b) for b in new_chain_dicts]
        if len(new_chain) <= len(self.chain):
            return False
        if not self.is_valid(new_chain):
            return False
        self.chain = new_chain
        # drop pending tx that are already on the new chain
        seen = {tx.get("id") for blk in self.chain for tx in blk.transactions}
        self.pending = [tx for tx in self.pending if tx.get("id") not in seen]
        return True

    # ── serialization ──

    def to_dict(self) -> dict:
        return {
            "difficulty": self.difficulty,
            "chain": [b.to_dict() for b in self.chain],
            "pending": list(self.pending),
        }

    def load_dict(self, d: dict) -> None:
        self.difficulty = d.get("difficulty", DIFFICULTY)
        self.chain = [Block.from_dict(b) for b in d["chain"]]
        self.pending = list(d.get("pending", []))

    # ── queries ──

    def all_threats(self) -> list[dict]:
        """Flatten every threat tx in the chain, newest first."""
        out = [tx for blk in self.chain for tx in blk.transactions]
        out.sort(key=lambda t: t.get("timestamp", 0), reverse=True)
        return out

    def search(self, query: str) -> list[dict]:
        q = query.strip().lower()
        if not q:
            return []
        hits = []
        for tx in self.all_threats():
            haystack = " ".join([
                tx.get("title", ""),
                tx.get("description", ""),
                tx.get("threat_type", ""),
                tx.get("severity", ""),
                tx.get("submitter_name", ""),
                " ".join(tx.get("iocs", [])),
            ]).lower()
            if q in haystack:
                hits.append(tx)
        return hits
