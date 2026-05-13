"""
RSA cryptography for ThreatChain.

Each organization owns an RSA keypair. The public key is its on-chain identity.
The private key signs every threat submission so other nodes can verify the
threat really came from that organization and was not tampered with in transit.
"""

import base64
import json
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.exceptions import InvalidSignature


def generate_keypair():
    """Create a new 2048-bit RSA keypair. Returns (private_pem, public_pem) strings."""
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("utf-8")
    public_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode("utf-8")
    return private_pem, public_pem


def _load_private(private_pem: str):
    return serialization.load_pem_private_key(private_pem.encode("utf-8"), password=None)


def _load_public(public_pem: str):
    return serialization.load_pem_public_key(public_pem.encode("utf-8"))


def canonical_bytes(payload: dict) -> bytes:
    """Serialize a dict deterministically so signatures are reproducible."""
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sign(private_pem: str, payload: dict) -> str:
    """Sign a dict with RSA-PSS-SHA256. Returns a base64 string."""
    key = _load_private(private_pem)
    signature = key.sign(
        canonical_bytes(payload),
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256(),
    )
    return base64.b64encode(signature).decode("utf-8")


def verify(public_pem: str, payload: dict, signature_b64: str) -> bool:
    """Return True iff `signature_b64` is a valid signature of `payload` by `public_pem`."""
    try:
        key = _load_public(public_pem)
        key.verify(
            base64.b64decode(signature_b64),
            canonical_bytes(payload),
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256(),
        )
        return True
    except (InvalidSignature, ValueError, TypeError):
        return False


def fingerprint(public_pem: str) -> str:
    """Short human-readable fingerprint for a public key (first 16 hex chars of SHA-256)."""
    import hashlib
    return hashlib.sha256(public_pem.encode("utf-8")).hexdigest()[:16]
