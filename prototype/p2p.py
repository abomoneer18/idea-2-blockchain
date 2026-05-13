"""
P2P gossip for ThreatChain.

Each node exposes HTTP endpoints. Peers learn about each other via /peers/register,
then call each other's /chain endpoints to compare lengths and adopt the
longest valid chain (Nakamoto consensus, simplified).

Failure mode: peers go up and down freely. We never raise — unreachable peers
are simply skipped.
"""

from __future__ import annotations

import requests

REQ_TIMEOUT = 3.0


def fetch_chain(peer_url: str) -> list[dict] | None:
    try:
        r = requests.get(f"{peer_url}/api/chain", timeout=REQ_TIMEOUT)
        if r.status_code == 200:
            return r.json().get("chain", [])
    except requests.RequestException:
        return None
    return None


def fetch_orgs(peer_url: str) -> dict | None:
    try:
        r = requests.get(f"{peer_url}/api/orgs", timeout=REQ_TIMEOUT)
        if r.status_code == 200:
            return r.json().get("orgs", {})
    except requests.RequestException:
        return None
    return None


def announce_to_peer(peer_url: str, self_url: str) -> bool:
    try:
        r = requests.post(
            f"{peer_url}/api/peers/register",
            json={"url": self_url},
            timeout=REQ_TIMEOUT,
        )
        return r.status_code == 200
    except requests.RequestException:
        return False


def broadcast_tx(peers: list[str], tx: dict) -> int:
    """Send a new transaction to every peer. Returns count of peers that accepted it."""
    accepted = 0
    for p in peers:
        try:
            r = requests.post(f"{p}/api/threats/receive", json=tx, timeout=REQ_TIMEOUT)
            if r.status_code == 200:
                accepted += 1
        except requests.RequestException:
            continue
    return accepted


def resolve_consensus(blockchain, peers: list[str], merge_orgs_cb) -> tuple[bool, int]:
    """
    Pull each peer's chain, adopt the longest valid one, and merge any orgs the
    peer knows about so we can verify signatures on its blocks.

    Returns (replaced?, peer_count_reached).
    """
    reached = 0
    best = None
    best_len = len(blockchain.chain)

    for p in peers:
        peer_chain = fetch_chain(p)
        if peer_chain is None:
            continue
        reached += 1
        if len(peer_chain) > best_len:
            peer_orgs = fetch_orgs(p) or {}
            merge_orgs_cb(peer_orgs)
            if blockchain.replace_chain(peer_chain):
                best = peer_chain
                best_len = len(peer_chain)

    return (best is not None), reached
