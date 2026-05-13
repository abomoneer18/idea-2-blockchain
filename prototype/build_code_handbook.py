"""
Build a comprehensive code-explanation handbook for the ThreatChain project.

This is written for a student who is not deeply experienced with coding. It walks
through every source file, explains every imported library, every function, and
the role of each block of code, and includes likely defense-day questions with
prepared answers.

Output: ThreatChain_Code_Handbook.docx (about 25 pages).
"""

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING, WD_BREAK
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUTPUT = r"C:\Users\abdul\OneDrive\Desktop\idea 2 blockchain\ThreatChain_Code_Handbook.docx"

DOC = Document()


# ─────────────────────────── styling ───────────────────────────

style = DOC.styles["Normal"]
style.font.name = "Calibri"
style.font.size = Pt(11)
style.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
style.paragraph_format.line_spacing = 1.2
style.paragraph_format.space_after = Pt(6)

for h_idx, h_size, h_color in [(1, 22, "1f3864"), (2, 16, "2e75b6"), (3, 13, "5b6f8f")]:
    h = DOC.styles[f"Heading {h_idx}"]
    h.font.name = "Calibri"
    h.font.size = Pt(h_size)
    h.font.bold = True
    h.font.color.rgb = RGBColor.from_string(h_color)
    h.paragraph_format.space_before = Pt(18 if h_idx == 1 else 12)
    h.paragraph_format.space_after = Pt(6)

for section in DOC.sections:
    section.left_margin = section.right_margin = Inches(0.9)
    section.top_margin = section.bottom_margin = Inches(0.9)

# centered footer page number
footer_p = DOC.sections[0].footer.paragraphs[0]
footer_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
fld_begin = OxmlElement("w:fldChar"); fld_begin.set(qn("w:fldCharType"), "begin")
instr = OxmlElement("w:instrText"); instr.text = "PAGE"
fld_end = OxmlElement("w:fldChar"); fld_end.set(qn("w:fldCharType"), "end")
r = footer_p.add_run().element
r.append(fld_begin); r.append(instr); r.append(fld_end)


# ─────────────────────────── helpers ───────────────────────────

def body(text, *, justify=True, italic=False):
    p = DOC.add_paragraph()
    if justify: p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p.add_run(text)
    if italic: r.italic = True
    return p

def h1(t): return DOC.add_heading(t, level=1)
def h2(t): return DOC.add_heading(t, level=2)
def h3(t): return DOC.add_heading(t, level=3)

def code(text):
    """Render a fixed-width 'code' paragraph with shading."""
    p = DOC.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.3)
    p.paragraph_format.space_after = Pt(8)
    r = p.add_run(text)
    r.font.name = "Consolas"
    r.font.size = Pt(9.5)
    r.font.color.rgb = RGBColor.from_string("23272e")
    # add light gray background using XML
    rPr = r._element.get_or_add_rPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), "f5f5f7")
    rPr.append(shd)
    return p

def bullet(t):
    p = DOC.add_paragraph(t, style="List Bullet")
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    return p

def page_break():
    p = DOC.add_paragraph()
    p.add_run().add_break(WD_BREAK.PAGE)

def qa(question, answer):
    """A small Q&A pair, used at the end of each file's section."""
    p = DOC.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p.add_run("Q.  "); r.bold = True; r.font.color.rgb = RGBColor.from_string("c2410c")
    r2 = p.add_run(question); r2.bold = True
    p = DOC.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_after = Pt(10)
    r = p.add_run("A.  "); r.bold = True; r.font.color.rgb = RGBColor.from_string("059669")
    p.add_run(answer)


# ═══════════════════════════════════════════════════════════════════════════════
# COVER
# ═══════════════════════════════════════════════════════════════════════════════

p = DOC.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
for _ in range(6): p.add_run().add_break()
r = p.add_run("ThreatChain"); r.font.size = Pt(40); r.bold = True
r.font.color.rgb = RGBColor.from_string("1f3864"); r.font.name = "Calibri"

p = DOC.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Code Handbook"); r.font.size = Pt(22); r.italic = True
r.font.color.rgb = RGBColor.from_string("2e75b6")

p = DOC.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("A file-by-file explanation of the source code,\nwritten for defense preparation.")
r.font.size = Pt(13)

for _ in range(10): DOC.add_paragraph()

for label, value in [
    ("Project",     "ThreatChain — Decentralized Threat Intelligence Sharing"),
    ("Author",      "[Student Name]"),
    ("Supervisor",  "[Supervisor]"),
    ("Date",        "May 2026"),
]:
    p = DOC.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(label + ":  "); r.bold = True
    p.add_run(value)

page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# HOW TO READ THIS HANDBOOK
# ═══════════════════════════════════════════════════════════════════════════════

h1("How to Read This Handbook")

body(
    "This handbook walks through every Python source file in the ThreatChain prototype. "
    "It is written for someone who is comfortable reading instructions but not necessarily "
    "an expert programmer. The goal is that, after working through this document, you can "
    "open any file in your project, point at any piece of code, and explain in plain "
    "language what it does and why.")

body(
    "Each file is covered in the same fixed format:")
bullet("Purpose — one paragraph: why this file exists and what role it plays in the system.")
bullet("Libraries used — every imported module, with one or two sentences of explanation.")
bullet("Walkthrough — the code is divided into logical pieces and each piece is explained.")
bullet("Defense Q&A — three or four likely examiner questions with prepared answers.")

body(
    "The files are presented in the order they conceptually build on each other:")
for line in [
    "1. crypto_utils.py — the cryptographic foundation (RSA keys, signing, verifying).",
    "2. blockchain.py — the heart of the project: blocks, the chain, proof-of-work, validation.",
    "3. storage.py — saving and loading the chain and registries to JSON on disk.",
    "4. p2p.py — talking to other nodes over the network.",
    "5. app.py — the Flask web application that ties everything together.",
    "6. mitigations.py — the curated catalog of mitigation playbooks and detection links.",
    "7. pdf_report.py — generating the per-threat PDF report.",
]:
    bullet(line)

body(
    "It is recommended to read straight through the first time, then to revisit each "
    "section as you study before the defense. The defense Q&A at the end of each section "
    "is the most exam-relevant material — memorise those.")

page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# 1. crypto_utils.py
# ═══════════════════════════════════════════════════════════════════════════════

h1("1. crypto_utils.py — RSA Keys, Signing, and Verification")

h2("Purpose")
body(
    "This file is the cryptographic foundation of the entire project. Whenever an "
    "organization is registered, this file generates its RSA keypair. Whenever a threat is "
    "submitted, this file signs it with the submitter's private key. Whenever a node "
    "receives a threat from a peer, this file verifies that the signature is valid. If you "
    "remove this file, every signature in the system is forged and the chain becomes "
    "untrustworthy.")

h2("Libraries Used")

body("The file imports four things from the cryptography library and two standard-library modules:")
bullet("base64 — converts binary data (the signature bytes) into safe ASCII text that can be stored in JSON.")
bullet("json — used inside the canonical_bytes function to convert a Python dictionary into a sorted, deterministic byte string.")
bullet("cryptography.hazmat.primitives.hashes — provides SHA-256, the cryptographic hash function used inside RSA-PSS.")
bullet("cryptography.hazmat.primitives.serialization — converts RSA keys between in-memory objects and PEM text (the readable -----BEGIN ... ----- format).")
bullet("cryptography.hazmat.primitives.asymmetric.padding — provides the PSS padding scheme used during signing and verification.")
bullet("cryptography.hazmat.primitives.asymmetric.rsa — the actual RSA algorithm (key generation, sign, verify).")
bullet("cryptography.exceptions.InvalidSignature — the exception that is raised when a signature does not verify; the code catches it to return False instead of crashing.")

h2("Code Walkthrough")

h3("generate_keypair()")
code(
    "def generate_keypair():\n"
    "    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)\n"
    "    private_pem = private_key.private_bytes(...).decode(\"utf-8\")\n"
    "    public_pem  = private_key.public_key().public_bytes(...).decode(\"utf-8\")\n"
    "    return private_pem, public_pem"
)
body(
    "This function creates a brand-new RSA keypair (one private key and one public key). "
    "The key size is 2048 bits, which is the modern industry minimum for RSA. The number "
    "65537 is the standard public exponent — it is a small prime that makes verification "
    "fast and is recommended by NIST. Both keys are converted to PEM text format so they "
    "can be saved as plain strings inside the organization registry JSON file.")

h3("canonical_bytes(payload)")
code(
    "def canonical_bytes(payload: dict) -> bytes:\n"
    "    return json.dumps(payload, sort_keys=True, separators=(\",\", \":\")).encode(\"utf-8\")"
)
body(
    "Before signing or verifying anything, the transaction has to be turned into bytes in a "
    "completely deterministic way. If two computers serialise the same dictionary into "
    "slightly different JSON (different key order, extra whitespace), they will produce "
    "different bytes and therefore different signatures. This function eliminates that "
    "problem by sorting the keys alphabetically and removing all whitespace. Every node "
    "that runs this function on the same data gets identical bytes, so signatures verify "
    "correctly regardless of which machine produced them.")

h3("sign(private_pem, payload)")
code(
    "def sign(private_pem, payload):\n"
    "    key = _load_private(private_pem)\n"
    "    signature = key.sign(\n"
    "        canonical_bytes(payload),\n"
    "        padding.PSS(mgf=padding.MGF1(hashes.SHA256()),\n"
    "                    salt_length=padding.PSS.MAX_LENGTH),\n"
    "        hashes.SHA256(),\n"
    "    )\n"
    "    return base64.b64encode(signature).decode(\"utf-8\")"
)
body(
    "Signing turns a dictionary into a base64 string that proves 'whoever holds the private "
    "key vouches for this exact dictionary.' The line padding.PSS(...) chooses the modern "
    "probabilistic signature scheme PSS instead of the older PKCS#1 v1.5; PSS has stronger "
    "mathematical security proofs. SHA-256 is the hash function applied to the data before "
    "RSA mathematics runs. The result is raw bytes; base64.b64encode turns those bytes into "
    "printable ASCII so the signature can live inside a JSON document.")

h3("verify(public_pem, payload, signature_b64)")
code(
    "def verify(public_pem, payload, signature_b64) -> bool:\n"
    "    try:\n"
    "        key = _load_public(public_pem)\n"
    "        key.verify(\n"
    "            base64.b64decode(signature_b64),\n"
    "            canonical_bytes(payload),\n"
    "            padding.PSS(...),\n"
    "            hashes.SHA256(),\n"
    "        )\n"
    "        return True\n"
    "    except (InvalidSignature, ValueError, TypeError):\n"
    "        return False"
)
body(
    "Verification is the mirror image of signing. The verifier holds the public key (not "
    "the private one) and runs the same PSS + SHA-256 routine on the same canonical bytes. "
    "If everything matches, no exception is raised and the function returns True. If the "
    "signature was forged, the data was tampered with, or the wrong public key is used, the "
    "library raises InvalidSignature, which the code catches and converts to a clean False. "
    "The try/except wrapper is important — without it, a single bad signature would crash "
    "the whole node.")

h3("fingerprint(public_pem)")
code(
    "def fingerprint(public_pem):\n"
    "    import hashlib\n"
    "    return hashlib.sha256(public_pem.encode(\"utf-8\")).hexdigest()[:16]"
)
body(
    "A 2048-bit RSA public key is hundreds of characters long. Showing it in the UI would "
    "be unreadable. The fingerprint is the first 16 hex characters of SHA-256 of the key — "
    "a short, unique identifier that points to one specific organization. The user sees the "
    "fingerprint on their dashboard; the full key stays in the registry.")

h2("Defense Q&A")
qa("Why is the key size 2048 bits and not 1024 or 4096?",
   "1024 bits is no longer considered secure; NIST deprecated it in 2013. 4096 bits is "
   "more secure but signs and verifies more slowly, and for the use case of signing short "
   "threat reports, 2048 is the standard industry choice. It is the minimum recommended by "
   "NIST FIPS 186-5 and is what most production systems use.")
qa("Why use RSA-PSS instead of the simpler PKCS#1 v1.5?",
   "PSS is a probabilistic padding scheme: it injects fresh random bytes (the salt) on "
   "every signature, so signing the same message twice produces two different signatures. "
   "This randomization gives PSS stronger formal security proofs and protects against some "
   "fault attacks that affect the deterministic PKCS#1 v1.5 scheme. NIST FIPS 186-5 "
   "recommends PSS for new designs.")
qa("Why canonical JSON and not just json.dumps?",
   "Two computers must agree on the exact bytes before they can agree on a signature. "
   "Plain json.dumps does not guarantee key order and may add whitespace, so two machines "
   "can produce different bytes for the same data and get different signatures. Sorting "
   "keys and removing whitespace makes the serialization deterministic; every node that "
   "runs the function gets the same bytes and therefore the same signature.")
qa("If an attacker steals an organization's private key, what happens?",
   "The attacker can sign threats in that organization's name and the network will accept "
   "them as authentic. This is identical to the situation in PGP, in TLS certificates, and "
   "in cryptocurrency wallets. Mitigation is to protect the private key with file-system "
   "permissions or, for production, encrypted-at-rest storage using the cryptography "
   "library's BestAvailableEncryption. Future work in the project documentation lists this "
   "as a planned hardening step.")

page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# 2. blockchain.py
# ═══════════════════════════════════════════════════════════════════════════════

h1("2. blockchain.py — Blocks, the Chain, and Proof-of-Work")

h2("Purpose")
body(
    "This file is the heart of the project. It defines what a Block is, what a Blockchain "
    "is, how new blocks are mined using Proof-of-Work, and how the chain is validated. "
    "Without this file, ThreatChain is just an ordinary web application; with it, it is "
    "actually a blockchain.")

h2("Libraries Used")
bullet("hashlib — Python's built-in cryptographic-hash library. Provides SHA-256, the hash function used to compute every block hash.")
bullet("json — used by the canonical_bytes function (imported from crypto_utils) when serialising the block header for hashing.")
bullet("time — provides Unix timestamps for blocks and transactions.")
bullet("uuid — generates a unique identifier (UUID4) for every threat transaction so that duplicates can be detected.")
bullet("dataclasses — a Python feature that lets you define a class with named fields very concisely (used to define the Block).")
bullet("typing.Callable — used for type hints on the mining-progress callback.")
bullet("crypto_utils — the local module above, used here to access canonical_bytes, sign, and verify.")

h2("Constants at the Top")
code("DIFFICULTY = 4\n"
     "GENESIS_PREV_HASH = \"0\" * 64")
body(
    "DIFFICULTY is the Proof-of-Work setting: the SHA-256 hash of a valid block must begin "
    "with this many zero hex characters. At difficulty 4, mining a block usually completes "
    "in under one second on a modern computer; raising the number makes mining "
    "exponentially slower. GENESIS_PREV_HASH is a string of 64 zero characters used as the "
    "previous-block hash of the very first block, because there is no real previous block.")

h2("Transaction Helpers")

h3("make_threat_tx(...)")
body(
    "This function builds a complete threat transaction dictionary, signs it, and returns "
    "it. The dictionary contains the submitter's identity, the threat content (type, "
    "severity, title, description, indicators, mitigation, GitHub links), and a fresh "
    "UUID. The signature is added last; before signing, the dictionary is canonicalised by "
    "the sign function from crypto_utils, so any other node that holds the submitter's "
    "public key can reproduce the exact bytes and verify the signature.")

h3("verify_tx(tx)")
body(
    "Given a complete signed transaction, this function pulls out the signature and the "
    "submitter's public key, then asks crypto_utils.verify whether the signature is valid. "
    "If either the signature field or the public-key field is missing, or if the signature "
    "does not check out, the function returns False. Every block-validation pass calls "
    "verify_tx on every transaction inside the block.")

h2("The Block Dataclass")
code("@dataclass\n"
     "class Block:\n"
     "    index: int\n"
     "    timestamp: float\n"
     "    transactions: list[dict]\n"
     "    previous_hash: str\n"
     "    nonce: int = 0\n"
     "    hash: str = \"\"")
body(
    "A block has six fields: its sequential index (0 for the genesis block, 1, 2, … "
    "thereafter); its creation timestamp; a list of transactions inside it; the hash of "
    "the previous block (this is what links blocks together into a chain); a nonce, which "
    "is the integer found during mining; and the block's own hash. The @dataclass "
    "decorator generates the boilerplate __init__ and __repr__ automatically, saving "
    "many lines of code.")

h3("header(self)")
body(
    "Returns a dictionary containing everything except the hash field itself. The block's "
    "hash is computed by hashing this dictionary; if the hash were included in its own "
    "input, the computation would be circular.")

h3("compute_hash(self)")
code("def compute_hash(self):\n"
     "    return hashlib.sha256(canonical_bytes(self.header())).hexdigest()")
body(
    "Turns the header dictionary into deterministic canonical JSON bytes, then applies "
    "SHA-256, then converts the resulting bytes to a 64-character hexadecimal string. "
    "This is the function called both during mining and during validation.")

h3("mine(self, difficulty)")
code("def mine(self, difficulty=DIFFICULTY):\n"
     "    target = \"0\" * difficulty\n"
     "    self.nonce = 0\n"
     "    while True:\n"
     "        h = self.compute_hash()\n"
     "        if h.startswith(target):\n"
     "            self.hash = h\n"
     "            return\n"
     "        self.nonce += 1")
body(
    "Proof-of-Work in plain English: try one nonce, compute the hash, see whether the hash "
    "starts with the required number of zeros. If yes, that nonce is the answer — save the "
    "hash and stop. If no, increment the nonce and try again. There is no shortcut; the "
    "only way to find a valid nonce is to try many of them in sequence. At difficulty 4, "
    "the answer is found in tens of thousands of attempts on average.")

h2("The Blockchain Class")

h3("__init__ and the genesis block")
body(
    "When a Blockchain object is created, it immediately calls _add_genesis, which builds "
    "block index 0 (empty transaction list, previous_hash of 64 zeros) and mines it. From "
    "that point on, every subsequent block references the previous block's hash in its "
    "previous_hash field, creating the chain.")

h3("add_transaction(tx)")
body(
    "Verifies the signature on the transaction (rejects it if invalid). Checks that the "
    "transaction's UUID does not already exist in the pending list or in any past block "
    "(rejects it if it would be a duplicate). If both checks pass, adds the transaction to "
    "the pending list, waiting to be mined into the next block.")

h3("mine_pending()")
body(
    "Takes the entire pending-transactions list, packages it into a new block whose index "
    "is one greater than the last block's, mines it (finds the valid nonce), appends the "
    "block to the chain, and clears the pending list. This is the function called every "
    "time the dashboard's Submit IOC form is used.")

h3("is_valid(chain)")
body(
    "Walks the chain block by block and asserts four invariants: the recomputed hash "
    "matches the stored hash; the hash begins with the required number of zeros; the "
    "previous-hash field links correctly to the preceding block; and every transaction "
    "inside the block has a verifying signature. Any single failure makes the whole chain "
    "invalid. This is the function that detects tampering during the tamper-test demo.")

h3("replace_chain(new_chain_dicts)")
body(
    "Implements the longest-valid-chain rule. Given a chain received from a peer, the "
    "function refuses to replace the local chain unless the peer's chain is strictly "
    "longer than the local one AND passes is_valid. This prevents an attacker from rolling "
    "back the chain by feeding a short forged chain, and prevents accidental corruption "
    "from short broken chains.")

h3("all_threats() and search(query)")
body(
    "Helper methods that flatten the chain into a single list of threats (sorted newest "
    "first) and that perform a case-insensitive substring search across titles, "
    "descriptions, types, severities, submitters, and indicators. These power the dashboard "
    "live-feed and search pages.")

h2("Defense Q&A")
qa("Why is Proof-of-Work needed in a permissioned network?",
   "It is not strictly needed; for a production permissioned network, Proof-of-Authority "
   "is the correct choice and is listed in the future-work section. PoW was used in the "
   "prototype because it visibly demonstrates the consensus concept: anyone watching the "
   "demo can literally see that a block was 'hard' to compute, which makes it intuitive "
   "why the chain cannot be cheaply rewritten.")
qa("What stops me from changing block 3 and recomputing every later block's hash?",
   "Two things. First, each block's hash must satisfy the difficulty target — so "
   "rewriting block 3, then 4, then 5, … requires re-mining every block, which is "
   "computationally expensive. Second, even if you do all that work, you still have a "
   "shorter chain than the honest peers; on the next consensus sync, the longest-valid-"
   "chain rule causes your tampered chain to be discarded and replaced by the honest one.")
qa("Why is the genesis block hash not zero?",
   "Because the genesis block is mined like any other block: its content (empty "
   "transaction list, previous_hash of 64 zeros) is hashed, and the nonce is searched "
   "until the SHA-256 of that content satisfies the difficulty target. The previous_hash "
   "of the genesis block is 64 zeros — that is what is constant; the genesis hash itself "
   "is just whatever value the miner happened to find.")
qa("Why is the transaction UUID checked against both pending and the chain?",
   "To prevent duplicate transactions. If a malicious or buggy peer rebroadcasts an old "
   "transaction, we do not want it to be mined into a second block. Checking the UUID "
   "everywhere — pending list and every block on the chain — catches both immediate and "
   "delayed replays.")

page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# 3. storage.py
# ═══════════════════════════════════════════════════════════════════════════════

h1("3. storage.py — JSON Persistence")

h2("Purpose")
body(
    "Each node needs to remember three things across restarts: the blockchain itself, the "
    "list of organizations it knows about (with their keypairs and fingerprints), and the "
    "list of peer URLs. This file saves those three pieces of state to plain JSON files in "
    "the node's data directory and loads them back when the application starts.")

h2("Libraries Used")
bullet("json — built-in module for reading and writing JSON files.")
bullet("os and pathlib.Path — for building safe file paths that work on Windows and Linux.")
bullet("threading.RLock — a reentrant lock used to prevent two threads from writing to the same JSON file simultaneously.")
bullet("time — for the registered-at timestamp on each organization.")
bullet("blockchain — the local module above, because the NodeStore holds a reference to a Blockchain instance.")

h2("The NodeStore Class")
body(
    "A NodeStore object knows the path to one node's data folder and exposes simple "
    "save/load methods. The three JSON files it manages are:")
bullet("chain.json — the entire blockchain (difficulty, list of blocks, pending list).")
bullet("orgs.json — the per-node organization registry: a dictionary keyed by fingerprint, with name, sector, public key, and private key (where applicable).")
bullet("peers.json — a list of peer URLs.")

h3("save_chain() and load_chain()")
body(
    "save_chain calls blockchain.to_dict() (defined in blockchain.py) to get a "
    "JSON-serialisable representation of the chain, then writes it to chain.json with the "
    "thread lock held. load_chain reads the JSON back and feeds it to blockchain."
    "load_dict, which rebuilds the in-memory chain. The lock prevents corruption if two "
    "requests try to save at the same time.")

h3("register_org(name, sector, public_pem, private_pem)")
body(
    "Reads the current registry, adds an entry keyed by the fingerprint of the public key, "
    "stores name + sector + both keys + the current timestamp, and writes the registry "
    "back to disk. When a remote organization is learnt about via peer gossip, "
    "private_pem is None — that organization can be verified locally because we have the "
    "public key, but we cannot submit on its behalf because we do not have the private "
    "key. Only the originating node ever holds its own private key.")

h3("add_peer(url) / remove_peer(url) / load_peers()")
body(
    "Simple list operations: append a new URL if not present, remove a URL if present, "
    "return the current sorted list. Each operation is wrapped in the lock and persists "
    "the result to peers.json.")

h2("Defense Q&A")
qa("Why use plain JSON files instead of a database server?",
   "For a demonstrable prototype, JSON is the simplest choice: no database to install, "
   "no schema to migrate, no server to keep running. The chain is small (kilobytes per "
   "block) so the read/write cost is negligible. For a production deployment with "
   "thousands of nodes and millions of threats, the storage module would be the natural "
   "place to swap in SQLite, PostgreSQL, or LevelDB — the rest of the project would not "
   "change.")
qa("Why hold the private key in plain JSON?",
   "Because the prototype is single-machine and intended to be opened in a text editor "
   "during the defense to show the audience what is actually on disk. For production, the "
   "private key would be encrypted at rest using the cryptography library's "
   "BestAvailableEncryption (passphrase-protected), or kept in a hardware security module "
   "(HSM) or operating-system keystore. This is in the future-work section.")
qa("What is the threading.RLock for?",
   "A reentrant lock prevents two threads from writing the same file at the same time. "
   "Flask handles each web request in a thread, and the JSON files are global state; "
   "without the lock, two simultaneous submissions could interleave their writes and "
   "corrupt the file. RLock allows the same thread to acquire the lock multiple times "
   "(for example, a save inside a load), which a plain Lock would not.")

page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# 4. p2p.py
# ═══════════════════════════════════════════════════════════════════════════════

h1("4. p2p.py — Peer-to-Peer Gossip")

h2("Purpose")
body(
    "Each node only knows about other nodes through this module. It provides four "
    "operations: register the local node with a peer, fetch a peer's chain or organization "
    "list, broadcast a new transaction to all peers, and resolve consensus by adopting the "
    "longest valid chain across peers.")

h2("Libraries Used")
bullet("requests — a small, popular HTTP client library that makes GET and POST calls in one line of code each.")

h2("The Module-Level Constant")
code("REQ_TIMEOUT = 3.0")
body(
    "Every HTTP call uses a 3-second timeout. If a peer is offline, slow, or unreachable, "
    "the call returns within three seconds rather than hanging the whole application. This "
    "is essential in a peer-to-peer system because peers come and go freely.")

h2("The Five Functions")

h3("fetch_chain(peer_url)")
body(
    "Makes a GET request to <peer_url>/api/chain and returns the chain field of the JSON "
    "response, or None if the peer is unreachable. The try/except around requests."
    "RequestException is what makes the peer-to-peer network resilient: a node never "
    "crashes because a peer is down.")

h3("fetch_orgs(peer_url)")
body(
    "Same pattern as fetch_chain, but for the organization registry. The remote endpoint "
    "deliberately strips private keys before responding, so this call only ever returns "
    "public material.")

h3("announce_to_peer(peer_url, self_url)")
body(
    "Sends a POST to <peer_url>/api/peers/register with the local node's public URL. The "
    "peer then records the local URL in its own peer list. After this call returns "
    "successfully, both nodes know about each other.")

h3("broadcast_tx(peers, tx)")
body(
    "Walks the list of known peers and sends a POST with the new transaction to each "
    "peer's /api/threats/receive endpoint. Returns the count of peers that accepted the "
    "transaction. Peers that timed out or returned an error are simply skipped — the "
    "function never raises.")

h3("resolve_consensus(blockchain, peers, merge_orgs_cb)")
body(
    "The function that implements the longest-valid-chain rule. It iterates over every "
    "peer, downloads each peer's chain, and asks the local Blockchain.replace_chain "
    "method whether to adopt it. replace_chain only swaps the local chain if the peer's "
    "chain is strictly longer and is fully valid; otherwise nothing changes. "
    "merge_orgs_cb is a callback that the caller (app.py) provides — it merges the peer's "
    "organization registry into the local one so that, after the swap, the local node has "
    "every public key needed to verify the signatures in the new chain.")

h2("Defense Q&A")
qa("Why HTTP and not a custom binary protocol?",
   "HTTP is universally supported, easy to test with curl or a browser, and trivial to "
   "secure with TLS in production. The performance overhead is negligible for chains "
   "exchanged once every few seconds. A binary protocol would be more efficient but would "
   "require writing both client and server code that does not exist today.")
qa("What happens during a network partition?",
   "Each side of the partition continues to mine its own blocks. When the partition "
   "heals, the next consensus sync picks the longer of the two chains. Any transactions "
   "that exist only on the discarded shorter chain are lost — this is the classic Nakamoto "
   "behaviour and is acceptable for threat intelligence because the same threats can be "
   "resubmitted.")
qa("Is this peer-to-peer protocol secure against an attacker injecting a forged chain?",
   "Yes, because is_valid is run on every block of the incoming chain before "
   "replace_chain accepts it. Forged blocks would fail the signature check, the "
   "Proof-of-Work check, or the previous-hash check, and the swap would be refused. The "
   "attacker would need valid private keys for the originating organizations of every "
   "transaction, which they do not have.")

page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# 5. app.py
# ═══════════════════════════════════════════════════════════════════════════════

h1("5. app.py — The Flask Web Application")

h2("Purpose")
body(
    "This is the file the user actually launches: it creates the Flask application, "
    "defines every page route (the URLs people visit in the browser) and every API "
    "endpoint (the URLs peer nodes call), and ties together the blockchain, the storage, "
    "the peer-to-peer module, the cryptography module, and the PDF generator.")

h2("Libraries Used")
bullet("argparse — built-in module for parsing command-line flags like --node, --port, --peer.")
bullet("secrets — built-in module for generating the Flask session-secret key cryptographically.")
bullet("threading — used to launch the background peer-announcement task at startup.")
bullet("pathlib — for file paths.")
bullet("Flask, render_template, request, session, redirect, url_for, jsonify, flash, abort, Response — the building blocks of the web framework. Each handles one specific aspect: rendering Jinja2 templates, reading form/query data, storing per-user session data, redirecting after POST, generating URLs, building JSON responses, showing one-time banner messages, returning an error, and sending binary responses (used for PDFs).")
bullet("blockchain — local module providing Blockchain and make_threat_tx.")
bullet("crypto_utils — local module providing fingerprint and generate_keypair.")
bullet("mitigations — local module providing MITIGATIONS catalog and get_playbook helper.")
bullet("pdf_report — local module providing build_threat_report.")
bullet("storage — local module providing NodeStore and data_dir_for.")
bullet("p2p — local module providing peer-to-peer functions.")

h2("The create_app Factory Function")
body(
    "Rather than declaring the Flask app at the module top level, the file wraps it in a "
    "create_app function. This pattern (called the 'application factory') is recommended "
    "in the Flask documentation because it allows the same code to launch many independent "
    "node instances (with different node names and ports) without interfering with each "
    "other. Each call to create_app returns a fresh Flask object that owns its own "
    "Blockchain, its own NodeStore, and its own Flask session secret.")

h3("Inside create_app: the helpers")
body(
    "Two small helper functions are defined inside the factory and used by the routes:")
bullet("current_org() — looks up the organization fingerprint stored in the user's session and returns the matching registry entry, or None if the user is not logged in.")
bullet("merge_orgs(remote_orgs) — used by the consensus-resolution flow to fold a peer's organization registry into the local one, stripping any private-key field for safety.")

h2("Page Routes")

body(
    "Each route is a Python function decorated with @app.route(...). Flask calls the "
    "function when the matching URL is requested and returns whatever the function "
    "returns to the browser. The page routes are:")

bullet("GET / — the landing page (landing.html).")
bullet("GET/POST /register — show the registration form, or process the form, generate a keypair, save the organization, and redirect to /dashboard.")
bullet("GET/POST /login — list registered organizations and switch the active one.")
bullet("GET /logout — clear the session and return to the landing page.")
bullet("GET /dashboard — the live threat feed; shows the latest 50 threats.")
bullet("GET/POST /dashboard/submit — the threat-submission form; on POST, signs the transaction, mines a new block, persists, and broadcasts to peers.")
bullet("GET /dashboard/explorer — the blockchain explorer; shows every block with its hash, previous_hash, nonce, and contained transactions.")
bullet("GET/POST /dashboard/network — peer management; on POST, adds, removes, or triggers a consensus sync.")
bullet("GET /dashboard/search — full-text search across all threats; calls Blockchain.search.")
bullet("GET /threats/<id>/report.pdf — generates and returns a per-threat PDF using pdf_report.build_threat_report.")

h2("API Routes")

body(
    "The API routes (under /api/) speak JSON instead of HTML and are used by peer nodes "
    "during consensus and gossip:")

bullet("GET /api/chain — returns the full blockchain as JSON.")
bullet("GET /api/threats — returns the flattened threat list.")
bullet("GET /api/stats — returns a small summary (block count, threat count, organization count, peer count, pending count).")
bullet("GET /api/orgs — returns the public registry (with private keys stripped).")
bullet("POST /api/threats/receive — accept a gossiped transaction from a peer, verify, mine, save.")
bullet("POST /api/peers/register — accept a peer's announcement of its own URL.")
bullet("GET /api/peers — return the list of peer URLs.")
bullet("POST /api/sync — trigger consensus resolution against all peers.")

h2("Glue: filters, context processors, and startup")

body(
    "Three small pieces of glue make the templates simpler:")

bullet("@app.template_filter(\"timestamp\") — registers a Jinja filter that converts a Unix epoch number into a human-readable date string. Used inside templates as {{ tx.timestamp | timestamp }}.")
bullet("@app.context_processor — makes the MITIGATIONS dictionary and the get_playbook helper available in every template automatically, so the submit form's JavaScript can embed the catalog.")
bullet("def main() — the script entry point. Parses --node, --port, --peer flags via argparse, builds the Flask app, launches a daemon thread that announces this node to its peers, and runs Flask.")

h2("Defense Q&A")
qa("Why does each request create a Blockchain instance?",
   "It does not — the Blockchain is created exactly once, inside create_app, and held in "
   "app.config so every request handler sees the same instance. The factory pattern just "
   "lets us run multiple node processes side by side, each with its own Blockchain.")
qa("What does the Flask session do?",
   "Flask sessions are signed cookies stored in the user's browser. The application uses "
   "the session to remember which organization the user is acting as (the fingerprint of "
   "their public key). When the browser hits /dashboard, current_org() reads the cookie, "
   "looks up the organization in orgs.json, and returns the entry. No password is "
   "involved in the prototype, but adding one is in the future-work list.")
qa("Why are /api/* endpoints separate from the page routes?",
   "Because they speak different formats. The page routes return HTML for humans; the "
   "API routes return JSON for other nodes. Keeping them in separate URL prefixes makes "
   "it easy to extend, secure, or rate-limit the API independently of the human UI.")
qa("How does a new transaction propagate from the submitting node to all peers?",
   "In four steps: (1) the submitter's node signs the transaction; (2) it mines a new "
   "block locally and saves the chain; (3) it calls broadcast_tx, which POSTs the "
   "transaction to /api/threats/receive on each peer; (4) each peer verifies the "
   "signature, accepts the transaction, mines its own next block, and saves. After this "
   "the chains may differ by one block; the next consensus sync converges them.")

page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# 6. mitigations.py
# ═══════════════════════════════════════════════════════════════════════════════

h1("6. mitigations.py — The Curated Knowledge Catalog")

h2("Purpose")
body(
    "This file is the curated knowledge base of the project. It holds one entry per "
    "supported threat type (malware, phishing, ransomware, C2, vulnerability, DDoS, and a "
    "generic 'other' fallback). Each entry contains: a human-readable name, a one-line "
    "summary, a list of eight defensive steps, three authoritative external references, "
    "and three to four curated GitHub repositories with detection rules or trained "
    "models. The file is pure data: no logic except one small lookup helper.")

h2("Libraries Used")
body(
    "None at all besides Python's built-in features. Everything in this file is just a "
    "dictionary literal.")

h2("Structure of an Entry")
code(
    '"phishing": {\n'
    '    "name": "Phishing",\n'
    '    "summary": "Social-engineering attempts...",\n'
    '    "steps": [\n'
    '        "Deploy SPF, DKIM, DMARC...",\n'
    '        "Use a mail gateway with sandbox detonation...",\n'
    '        ...\n'
    '    ],\n'
    '    "references": [\n'
    '        {"name": "CISA — Phishing", "url": "https://..."},\n'
    '        ...\n'
    '    ],\n'
    '    "detection_models": [\n'
    '        {"name": "mitchellkrogza/Phishing.Database",\n'
    '         "url": "https://github.com/...",\n'
    '         "description": "Daily-updated list of active phishing domains..."},\n'
    '        ...\n'
    '    ],\n'
    '}'
)
body(
    "The same structure is repeated for every threat type. Adding a new type is as simple "
    "as adding another dictionary entry — no other file needs to change.")

h2("The get_playbook() Helper")
code("def get_playbook(threat_type):\n"
     "    return MITIGATIONS.get((threat_type or \"\").lower(), MITIGATIONS[\"other\"])")
body(
    "This one-line function looks up a playbook by threat type, falling back to the "
    "generic 'other' entry if the type is not recognised. The fallback guarantees that "
    "every threat — even one with a custom or misspelled type — still gets a playbook in "
    "the PDF report and on the dashboard.")

h2("Why is this catalog off-chain?")
body(
    "Defensive practices evolve as new tools and standards appear. Putting the catalog on "
    "the blockchain would mean any update has to be mined into a new block and would live "
    "forever, alongside the threat reports themselves. By keeping the catalog in source "
    "code, the project can ship updated playbooks at any time with a simple file edit, "
    "without rewriting history. The cryptographic provenance of threat reports is "
    "unaffected because the playbook is rendered into the PDF at request time but is not "
    "covered by the original submission's signature.")

h2("Defense Q&A")
qa("Who maintains the catalog in production?",
   "In a production deployment the catalog would be maintained as a separate, versioned, "
   "signed feed published by a trusted authority (a national CERT, for instance). Each "
   "node would download and verify the latest version. This is in the future-work list "
   "as 'Signed external catalog'.")
qa("Why list specific GitHub repositories — what if they go offline?",
   "Each repository is one of the most widely cited and longest-running open-source "
   "projects in its space (Yara-Rules/rules, SigmaHQ/sigma, redcanaryco/atomic-red-team, "
   "etc.). They are very unlikely to disappear, and if one does, replacing it is a "
   "single-line edit. The system tolerates missing links gracefully — the dashboard and "
   "PDF still render fine if a URL no longer works; users just cannot follow it.")
qa("Why eight steps and three references per threat type?",
   "Eight is enough to be substantive without overwhelming the reader. Three references "
   "consistently provide one each from NIST, MITRE, and CISA, which is the recognised "
   "triad of authoritative US-aligned guidance. The pattern is consistent across all "
   "threat types, which makes the PDFs predictable to scan.")

page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# 7. pdf_report.py
# ═══════════════════════════════════════════════════════════════════════════════

h1("7. pdf_report.py — Per-Threat PDF Reports")

h2("Purpose")
body(
    "When a defender clicks 'Download PDF Report' on a threat, this file builds a "
    "professionally-formatted PDF on demand. The PDF contains the threat content, the "
    "indicators of compromise, the submitter's mitigation, the standard mitigation "
    "playbook, the standard and submitter-provided detection resources, and the "
    "cryptographic provenance (block index, block hash, signature) needed to re-verify "
    "the report against the chain.")

h2("Libraries Used")
bullet("io — provides BytesIO, an in-memory buffer that ReportLab writes the PDF into. The buffer's contents are then returned as a byte string and streamed to the user's browser.")
bullet("time — for timestamp formatting.")
bullet("reportlab.lib.pagesizes.A4 — the page size (210mm x 297mm).")
bullet("reportlab.lib.styles — ParagraphStyle, getSampleStyleSheet — typography presets.")
bullet("reportlab.lib.units.cm — the centimeter unit for margins.")
bullet("reportlab.lib.enums — TA_LEFT, TA_JUSTIFY, TA_CENTER alignment constants.")
bullet("reportlab.platypus — SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether — the high-level layout API.")
bullet("reportlab.lib.colors.HexColor — colour parsing for navy/amber/rose accents.")

h2("Module Constants")
body(
    "Six named colours (NAVY, AMBER, ROSE, MUTED, LIGHT, DIVIDER) and a SEVERITY_COLOR "
    "mapping (critical = red-ish, high = orange-ish, medium = amber-ish, low = violet-ish) "
    "are defined at the top so they can be reused throughout the document. Centralising "
    "colour definitions keeps the look consistent.")

h2("Helper Functions")

h3("_styles()")
body(
    "Returns a dictionary of named paragraph styles (Title, Subtitle, Eyebrow, H2, Body, "
    "Mono, Link, MetaKey, MetaVal). Each style sets a font, size, leading (line height), "
    "colour, and spacing. The styles are used throughout the build_threat_report function.")

h3("_ts(value)")
body(
    "Formats a Unix epoch number as 'YYYY-MM-DD HH:MM:SS UTC'. Wrapped in a try/except so "
    "that malformed timestamps fall back to an em-dash instead of crashing PDF generation.")

h3("_split_mitigation(text)")
body(
    "Takes the submitter's free-text mitigation and decides whether it looks like a "
    "numbered list (e.g. '1. block IP\\n2. patch system'). If so, the prefixes are stripped "
    "and each item is returned as a separate bullet. Otherwise the whole text is returned "
    "as a single paragraph. This makes the PDF render mitigation lists nicely whether the "
    "submitter wrote one paragraph or eight numbered steps.")

h3("_footer(canvas, doc)")
body(
    "Draws the running footer on every page: project name on the left, page number "
    "centred, date on the right. Called by ReportLab for each page through the onFirstPage "
    "and onLaterPages parameters.")

h2("The Main Function: build_threat_report(tx, block_index, block_hash, playbook)")

body(
    "Takes a threat transaction dictionary, the index and hash of the block that sealed "
    "it, and the playbook dictionary (from mitigations.py). Returns the raw PDF bytes. "
    "The function builds the document in six numbered sections, in order:")

bullet("Section 1 — Description. The submitter's free-text description, rendered as a justified paragraph.")
bullet("Section 2 — Indicators of Compromise. The list of IOCs, rendered as a bulleted, monospace list.")
bullet("Section 3 — Recommended Mitigation. The submitter's specific mitigation (split into bullets by _split_mitigation if it looks like a list), or a fallback italic notice if blank.")
bullet("Section 4 — Standard Mitigation Playbook. The full playbook for the threat type: name, summary, eight steps, three authoritative references.")
bullet("Section 5 — Detection & Trained-Model Resources. Combines submitter-provided URLs with the curated standard catalog; the section is never empty.")
bullet("Section 6 — Cryptographic Provenance. A small table with threat ID, submitter, block index, block hash, submission timestamp, and the first 48 characters of the signature.")

body(
    "A closing italic paragraph reminds the reader that the document can be re-verified "
    "against the chain by any node holding the submitter's public key.")

h2("Defense Q&A")
qa("How is the PDF cryptographically linked to the chain?",
   "Section 6 of every PDF contains the block hash and the first 48 characters of the "
   "RSA-PSS signature, along with the threat's UUID. To verify the PDF, a downstream "
   "reader can use the threat ID to fetch the original transaction from any node's "
   "/api/chain endpoint, recompute the canonical bytes, and verify the signature against "
   "the submitter's published public key. If the PDF was altered, the signature on the "
   "chain still belongs to the original content and the alteration is detectable.")
qa("Why ReportLab and not WeasyPrint or HTML-to-PDF?",
   "ReportLab is pure Python with no external dependencies, no headless browser, and no "
   "system fonts to install. WeasyPrint would render nicer CSS but requires GTK/Pango "
   "libraries on the host. For a single-file Windows install for the demo, ReportLab is "
   "the simpler choice.")
qa("Could the PDF generation become slow with very long threat reports?",
   "In principle yes, but each transaction's free-text fields are short (a few hundred "
   "words at most). Empirically, PDF generation takes well under 100 milliseconds per "
   "report on commodity hardware. If the threat catalog grew to thousands of indicators "
   "per threat, the PDF would still generate in under a second.")

page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# CLOSING REVIEW
# ═══════════════════════════════════════════════════════════════════════════════

h1("Closing — Five Things to Have on the Tip of Your Tongue")

body(
    "If you only memorise five things from this handbook before walking into the defense, "
    "make them these:")

h3("1. Why is the chain tamper-evident?")
body(
    "Every block's hash is the SHA-256 of its content. Changing one byte of block 5 "
    "changes the hash of block 5, which breaks the previous_hash reference inside block 6, "
    "which breaks block 7, and so on. Every node will reject the modified chain because "
    "is_valid will fail on block 6.")

h3("2. Why is RSA-PSS used for signing?")
body(
    "Because it is the modern, probabilistic, formally-proven signature scheme recommended "
    "by NIST FIPS 186-5. It produces a fresh random signature on every call and is "
    "preferred over the older PKCS#1 v1.5 scheme.")

h3("3. Why is Proof-of-Work in the prototype but Proof-of-Authority for production?")
body(
    "Proof-of-Work is visibly slow and intuitive — it makes the consensus concept "
    "concrete during the demo. In a real permissioned network of verified organizations "
    "(Jordan CERT, banks, etc.), Proof-of-Authority is the correct choice: no mining, "
    "deterministic block times, dramatically lower energy use. This change preserves the "
    "rest of the architecture untouched.")

h3("4. What happens to a corrupted node?")
body(
    "is_valid detects the corruption immediately. The Network tab's 'Trigger Consensus "
    "Sync' fetches each peer's chain; the longest-valid one (which is the honest chain) "
    "replaces the corrupted local copy. This is exactly the experiment shown in the "
    "tamper-recovery demo.")

h3("5. Why is the playbook off-chain but the threat is on-chain?")
body(
    "Threats are evidence of attacks and must be permanent, signed, and tamper-evident — "
    "perfectly suited to a blockchain. Mitigation playbooks evolve as new defensive "
    "practices emerge; they must be updatable without rewriting history. Putting them in "
    "a versioned Python module gives the best of both worlds: the on-chain record is "
    "immutable, but the defensive guidance attached to it at display time is always "
    "current.")

DOC.save(OUTPUT)
print(f"Wrote: {OUTPUT}")
