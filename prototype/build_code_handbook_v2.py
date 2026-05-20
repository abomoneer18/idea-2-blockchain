"""
Rebuild the ThreatChain Code Handbook in plain, easy-English style.
Same structure as v1: file-by-file walkthrough with libraries, code blocks,
and defense Q&A. Different writing style: short sentences, common words.
"""

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING, WD_BREAK
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUTPUT = r"C:\Users\abdul\OneDrive\Desktop\idea 2 blockchain\ThreatChain_Code_Handbook_v2.docx"
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

footer_p = DOC.sections[0].footer.paragraphs[0]
footer_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
fld_begin = OxmlElement("w:fldChar"); fld_begin.set(qn("w:fldCharType"), "begin")
instr = OxmlElement("w:instrText"); instr.text = "PAGE"
fld_end = OxmlElement("w:fldChar"); fld_end.set(qn("w:fldCharType"), "end")
r = footer_p.add_run().element
r.append(fld_begin); r.append(instr); r.append(fld_end)


# ─────────────────────────── helpers ───────────────────────────
def body(text, *, justify=True):
    p = DOC.add_paragraph()
    if justify: p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.add_run(text)
    return p

def h1(t): return DOC.add_heading(t, level=1)
def h2(t): return DOC.add_heading(t, level=2)
def h3(t): return DOC.add_heading(t, level=3)

def code(text):
    p = DOC.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.3)
    p.paragraph_format.space_after = Pt(8)
    r = p.add_run(text)
    r.font.name = "Consolas"
    r.font.size = Pt(9.5)
    r.font.color.rgb = RGBColor.from_string("23272e")
    rPr = r._element.get_or_add_rPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), "f5f5f7")
    rPr.append(shd)
    return p

def bullet(t):
    p = DOC.add_paragraph(t, style="List Bullet")
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    return p

def page_break():
    DOC.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

def qa(question, answer):
    p = DOC.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p.add_run("Q.  "); r.bold = True; r.font.color.rgb = RGBColor.from_string("c2410c")
    r2 = p.add_run(question); r2.bold = True
    p = DOC.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_after = Pt(10)
    r = p.add_run("A.  "); r.bold = True; r.font.color.rgb = RGBColor.from_string("059669")
    p.add_run(answer)


# ─────────────────────────── COVER ───────────────────────────
p = DOC.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
for _ in range(6): p.add_run().add_break()
r = p.add_run("ThreatChain"); r.font.size = Pt(40); r.bold = True
r.font.color.rgb = RGBColor.from_string("1f3864"); r.font.name = "Calibri"

p = DOC.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Code Handbook"); r.font.size = Pt(22); r.italic = True
r.font.color.rgb = RGBColor.from_string("2e75b6")

p = DOC.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("A simple, file-by-file guide to the source code,\nwritten so anyone can follow it.")
r.font.size = Pt(13)

for _ in range(10): DOC.add_paragraph()
for label, value in [
    ("Project",    "ThreatChain — Decentralized Threat Intelligence Sharing"),
    ("Author",     "[Student Name]"),
    ("Supervisor", "[Supervisor]"),
    ("Date",       "May 2026"),
]:
    p = DOC.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(label + ":  "); r.bold = True
    p.add_run(value)

page_break()


# ─────────────────────────── HOW TO READ ───────────────────────────
h1("How to Read This Book")

body(
    "This handbook explains every Python file in the ThreatChain project. It is "
    "written for someone who can read code but is not an expert in Python or "
    "cryptography. The goal is simple: after reading this, you can open any "
    "file, point at any line, and say in your own words what it does.")

body("Every file is covered in the same four steps:")
bullet("Purpose — one paragraph saying what the file does and why it exists.")
bullet("Libraries used — what each imported package does, in one sentence each.")
bullet("Walkthrough — the code split into small pieces, each piece explained.")
bullet("Defense Q&A — questions a professor might ask, with prepared answers.")

body("The files appear in the order they build on each other:")
for line in [
    "1. crypto_utils.py — the key generator and signer (the cryptography layer).",
    "2. blockchain.py — the heart: blocks, the chain, mining, validation.",
    "3. storage.py — saving and loading data on disk.",
    "4. p2p.py — talking to other nodes over the internet.",
    "5. app.py — the Flask web application that ties everything together.",
    "6. mitigations.py — the playbook and detection-link catalog.",
    "7. pdf_report.py — making the per-threat PDF.",
]:
    bullet(line)

body(
    "Read it through once, then come back to each section as you study. The "
    "Q&A at the end of every chapter is the most important part for your "
    "defense — memorize those answers.")

page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# 1. crypto_utils.py
# ═══════════════════════════════════════════════════════════════════════════════
h1("1. crypto_utils.py — Keys, Signing, and Verifying")

h2("Purpose")
body(
    "This is the cryptography layer of the project. When an organization signs "
    "up, this file makes its RSA keys. When the organization submits a threat, "
    "this file signs it. When another node receives that threat, this file "
    "checks the signature. Without this file, anyone could fake any signature "
    "and the chain would be useless.")

h2("Libraries Used")
bullet("base64 — turns the signature bytes into safe text that fits inside JSON.")
bullet("json — turns Python dictionaries into a sorted text string (used inside canonical_bytes).")
bullet("hashes from cryptography — gives us SHA-256, the hash function used inside the signature.")
bullet("serialization from cryptography — turns keys into the PEM text format (-----BEGIN ...-----).")
bullet("padding from cryptography — gives us PSS, the modern padding scheme used by signatures.")
bullet("rsa from cryptography — the RSA algorithm itself (make keys, sign, verify).")
bullet("InvalidSignature — the error type raised when a signature does not match. We catch it and return False instead of crashing.")

h2("Walkthrough")

h3("generate_keypair()")
code(
    "def generate_keypair():\n"
    "    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)\n"
    "    private_pem = private_key.private_bytes(...).decode('utf-8')\n"
    "    public_pem  = private_key.public_key().public_bytes(...).decode('utf-8')\n"
    "    return private_pem, public_pem"
)
body(
    "This makes a fresh RSA keypair. The key size is 2048 bits — the modern "
    "minimum that NIST recommends. The number 65537 is the standard public "
    "exponent (it makes verifying signatures fast). Both keys come back as "
    "PEM text, which is just a long string that starts with -----BEGIN. We "
    "store these strings in the organization registry.")

h3("canonical_bytes(payload)")
code(
    "def canonical_bytes(payload: dict) -> bytes:\n"
    "    return json.dumps(payload, sort_keys=True, separators=(',', ':')).encode('utf-8')"
)
body(
    "Before signing or verifying, the data must be turned into bytes in a fixed "
    "way. If two computers produce different bytes for the same data, their "
    "signatures will not match. This function sorts the keys alphabetically and "
    "removes whitespace, so any computer that runs it on the same data gets the "
    "same bytes.")

h3("sign(private_pem, payload)")
code(
    "def sign(private_pem, payload):\n"
    "    key = _load_private(private_pem)\n"
    "    signature = key.sign(\n"
    "        canonical_bytes(payload),\n"
    "        padding.PSS(mgf=padding.MGF1(hashes.SHA256()),\n"
    "                    salt_length=padding.PSS.MAX_LENGTH),\n"
    "        hashes.SHA256())\n"
    "    return base64.b64encode(signature).decode('utf-8')"
)
body(
    "Signing produces a string that proves 'the holder of this private key "
    "approves this exact data'. The PSS line picks the modern padding scheme "
    "(better than the older PKCS#1 v1.5). The signature comes out as raw "
    "bytes; base64 turns those bytes into normal text so they can live inside "
    "a JSON document.")

h3("verify(public_pem, payload, signature_b64)")
code(
    "def verify(public_pem, payload, signature_b64) -> bool:\n"
    "    try:\n"
    "        key = _load_public(public_pem)\n"
    "        key.verify(base64.b64decode(signature_b64),\n"
    "                   canonical_bytes(payload),\n"
    "                   padding.PSS(...), hashes.SHA256())\n"
    "        return True\n"
    "    except (InvalidSignature, ValueError, TypeError):\n"
    "        return False"
)
body(
    "Verifying is the reverse of signing. The verifier holds the public key, "
    "not the private one. The library does the math; if everything checks out, "
    "no error is raised and we return True. If the signature is wrong, the "
    "library raises InvalidSignature, which we catch and turn into a clean "
    "False. The try/except wrapper is important — a bad signature must not "
    "crash the whole node.")

h3("fingerprint(public_pem)")
code(
    "def fingerprint(public_pem):\n"
    "    return hashlib.sha256(public_pem.encode('utf-8')).hexdigest()[:16]"
)
body(
    "A full 2048-bit public key is hundreds of characters long — too long to "
    "show in the UI. The fingerprint is a short 16-character SHA-256 of the "
    "key. It uniquely identifies the organization but fits on a single line.")

h2("Defense Q&A")
qa("Why 2048-bit RSA and not 1024 or 4096?",
   "1024 bits is no longer secure — NIST stopped recommending it in 2013. "
   "4096 bits is more secure but signs and verifies more slowly. For signing "
   "short threat reports, 2048 is the modern standard and is what most "
   "real systems use.")
qa("Why RSA-PSS instead of the older PKCS#1 v1.5?",
   "PSS uses fresh random bytes (salt) on every signature, so signing the "
   "same data twice gives two different signatures. This randomness gives "
   "PSS stronger formal security proofs and protects against some attacks "
   "that affect the older scheme. NIST FIPS 186-5 recommends PSS for new "
   "designs.")
qa("Why turn the data into 'canonical JSON' before signing?",
   "Two computers must produce the exact same bytes before they can produce "
   "the same signature. Plain JSON does not guarantee key order or whitespace, "
   "so two machines can get different bytes for the same data and break the "
   "signature. Sorting keys and removing whitespace makes the bytes the same "
   "everywhere.")
qa("What happens if an attacker steals an organization's private key?",
   "The attacker can sign threats in that organization's name and the network "
   "will believe them. This is exactly like stealing a PGP private key or a "
   "TLS certificate. The fix is to protect the private key — file permissions "
   "in the prototype, and encrypted storage or a hardware key in production. "
   "This is in the future-work list.")

page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# 2. blockchain.py
# ═══════════════════════════════════════════════════════════════════════════════
h1("2. blockchain.py — Blocks, the Chain, and Mining")

h2("Purpose")
body(
    "This file is the heart of the project. It defines what a Block is, what a "
    "Blockchain is, how new blocks are mined using Proof-of-Work, and how the "
    "chain is checked for validity. Without this file, ThreatChain is just an "
    "ordinary web app. With it, it is actually a blockchain.")

h2("Libraries Used")
bullet("hashlib — Python's built-in hashing library; we use SHA-256.")
bullet("json — used indirectly via canonical_bytes for stable serialization.")
bullet("time — gives Unix timestamps.")
bullet("uuid — makes a unique ID for each transaction so duplicates can be caught.")
bullet("dataclasses — a Python feature that defines a class with named fields in one short line.")
bullet("crypto_utils — the local module above; we use its canonical_bytes, sign, and verify.")

h2("Top-of-File Constants")
code("DIFFICULTY = 4\n"
     "GENESIS_PREV_HASH = '0' * 64")
body(
    "DIFFICULTY is the proof-of-work setting: a valid block's hash must start "
    "with this many zeros. At 4, mining usually finishes in under one second. "
    "Higher numbers make mining exponentially slower. GENESIS_PREV_HASH is "
    "a string of 64 zeros — used as the 'previous-hash' of the very first "
    "block, because there is no real previous block.")

h2("Transaction Helpers")

h3("make_threat_tx(...)")
body(
    "Builds a complete threat transaction (a dictionary), signs it, and returns "
    "it. The dictionary includes who sent it, what type of threat it is, the "
    "severity, the title, the description, the indicators, the mitigation, "
    "the GitHub links, and a fresh UUID. The signature is added last; it "
    "covers everything else.")

h3("verify_tx(tx)")
body(
    "Given a signed transaction, this function pulls out the signature and the "
    "submitter's public key, then asks crypto_utils.verify whether the "
    "signature is valid. If a field is missing or the signature does not check "
    "out, it returns False. Every chain-validation pass calls this on every "
    "transaction.")

h2("The Block Dataclass")
code("@dataclass\n"
     "class Block:\n"
     "    index: int\n"
     "    timestamp: float\n"
     "    transactions: list[dict]\n"
     "    previous_hash: str\n"
     "    nonce: int = 0\n"
     "    hash: str = ''")
body(
    "A block has six fields. The index counts up from 0. The timestamp is the "
    "creation time. The transactions list holds the threats inside this block. "
    "The previous_hash links this block to the one before it. The nonce is the "
    "number found during mining. The hash is the block's own identifier.")

h3("header(self)")
body(
    "Returns everything in the block except the hash field itself. We hash "
    "this header to get the block's hash. We exclude the hash field because "
    "we cannot use a value while computing it.")

h3("compute_hash(self)")
code("def compute_hash(self):\n"
     "    return hashlib.sha256(canonical_bytes(self.header())).hexdigest()")
body(
    "Turns the header into stable bytes (sorted JSON), runs SHA-256 on them, "
    "and returns the result as a 64-character hex string. Same function is "
    "used during mining and during validation.")

h3("mine(self, difficulty)")
code("def mine(self, difficulty=DIFFICULTY):\n"
     "    target = '0' * difficulty\n"
     "    self.nonce = 0\n"
     "    while True:\n"
     "        h = self.compute_hash()\n"
     "        if h.startswith(target):\n"
     "            self.hash = h\n"
     "            return\n"
     "        self.nonce += 1")
body(
    "Proof-of-Work in simple words: try a nonce, compute the hash, see if it "
    "starts with the right number of zeros. If yes, save the hash and stop. "
    "If no, increase the nonce by 1 and try again. There is no shortcut — "
    "the only way is to keep guessing. At difficulty 4, the answer is "
    "found in tens of thousands of tries.")

h2("The Blockchain Class")

h3("__init__ and the genesis block")
body(
    "When a Blockchain is created, it makes the genesis block: index 0, empty "
    "transactions, previous-hash of 64 zeros. It mines this block right away. "
    "From then on, every new block points to the previous one through its "
    "previous_hash field. That chain of pointers is what makes it a "
    "'block-chain'.")

h3("add_transaction(tx)")
body(
    "Checks the signature on the transaction first; if it is invalid, the "
    "transaction is rejected. Checks that the transaction's UUID is not already "
    "pending or already on the chain (rejects duplicates). If both checks pass, "
    "the transaction goes into the pending list to be mined into the next block.")

h3("mine_pending()")
body(
    "Takes every pending transaction, wraps them in a new block, mines the "
    "block (finds the valid nonce), adds the block to the chain, and clears "
    "the pending list. This is the function called every time someone clicks "
    "Submit on the dashboard.")

h3("is_valid(chain)")
body(
    "Walks the chain block by block and checks four things for each block: "
    "the stored hash matches the recomputed hash; the hash starts with the "
    "required zeros; the previous_hash links correctly to the block before; "
    "every transaction inside has a valid signature. If any one check fails, "
    "the whole chain is invalid. This is what detects tampering.")

h3("replace_chain(new_chain)")
body(
    "Implements the longest-valid-chain rule. Given a chain from a peer, this "
    "function refuses to replace the local chain unless the peer's chain is "
    "strictly longer AND fully valid. This stops an attacker from rolling back "
    "the chain with a short forged version.")

h3("all_threats() and search(query)")
body(
    "Helpers that flatten the chain into one list of threats (newest first) "
    "and search across titles, descriptions, types, severities, submitters, "
    "and indicators. These power the dashboard's live feed and search pages.")

h2("Defense Q&A")
qa("Why use Proof-of-Work in a permissioned network?",
   "We do not strictly need to — Proof-of-Authority is better for a real "
   "deployment, and it is in the future-work list. We used PoW in the "
   "prototype because it is visible: people can literally see the system "
   "search for a valid nonce. That makes the consensus idea concrete during "
   "the demo.")
qa("What stops me from editing block 3 and re-mining every later block?",
   "Two things. First, you would have to re-mine every block from 3 onwards, "
   "which is expensive. Second, even if you did all that work, you would have "
   "a chain that is the same length as the honest one, not longer. The next "
   "consensus sync would drop your version when an honest node has a chain "
   "of equal length.")
qa("Why is the genesis block's hash not zero?",
   "The genesis block is mined like any other block. Its content is fixed "
   "(empty list, previous-hash of 64 zeros), and the system searches for a "
   "nonce that makes the SHA-256 of that content start with the required "
   "zeros. The zeros are in the previous_hash field, not in the genesis "
   "block's own hash.")
qa("Why check the UUID against both pending and the chain?",
   "To prevent duplicates. If a buggy or malicious peer resends an old "
   "transaction, we do not want to mine it into a second block. Checking "
   "the UUID everywhere — pending list and every past block — catches both "
   "immediate and delayed replays.")

page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# 3. storage.py
# ═══════════════════════════════════════════════════════════════════════════════
h1("3. storage.py — Saving Data to Disk")

h2("Purpose")
body(
    "Each node has to remember three things between restarts: the chain itself, "
    "the list of organizations, and the list of peers. This file writes those "
    "three pieces of state as plain JSON files in the node's data folder, and "
    "reads them back when the app starts.")

h2("Libraries Used")
bullet("json — read and write JSON files.")
bullet("os and pathlib.Path — build file paths that work on Windows and Linux.")
bullet("threading.RLock — a lock that stops two threads from writing to the same file at the same time.")
bullet("time — for the registered-at timestamp on each organization.")
bullet("blockchain — the local module above; the NodeStore holds a reference to a Blockchain.")

h2("The NodeStore Class")
body("A NodeStore knows the path to one node's data folder and manages three JSON files:")
bullet("chain.json — the whole blockchain (difficulty, blocks, pending list).")
bullet("orgs.json — the organization registry: name, sector, public key, private key (if local), fingerprint, timestamp.")
bullet("peers.json — the list of peer URLs.")

h3("save_chain() and load_chain()")
body(
    "save_chain calls blockchain.to_dict() to get a JSON-friendly version of "
    "the chain, then writes it to chain.json while holding the thread lock. "
    "load_chain reads the JSON and feeds it to blockchain.load_dict, which "
    "rebuilds the in-memory chain. The lock makes sure two requests cannot "
    "corrupt the file by writing at the same time.")

h3("register_org(name, sector, public_pem, private_pem)")
body(
    "Reads the current registry, adds a new entry under the public key's "
    "fingerprint, saves the file. When a peer gossips us a new organization, "
    "private_pem is None — we have the public key so we can verify the "
    "organization's signatures, but we cannot sign on its behalf because we "
    "do not have its private key. Each private key only ever lives on the "
    "node where it was created.")

h3("add_peer / remove_peer / load_peers")
body(
    "Simple list operations: add a URL if not already there, remove a URL if "
    "present, return the current sorted list. Each one is wrapped in the "
    "thread lock and writes to peers.json.")

h2("Defense Q&A")
qa("Why JSON files instead of a database?",
   "For a demo prototype, JSON is the simplest choice: no database to install, "
   "no schema to manage, no extra server. The chain is small so read/write "
   "cost is tiny. For production with many nodes and many threats, the "
   "storage module is the natural place to swap in SQLite or PostgreSQL — "
   "no other file would need to change.")
qa("Why store the private key in plain text?",
   "Because the prototype is single-machine and we want to be able to open "
   "the file during the demo and show what is actually saved. In production, "
   "the private key would be encrypted at rest with a passphrase or kept in "
   "a hardware key. This is in the future-work section.")
qa("What is the threading.RLock for?",
   "Flask handles each web request in its own thread. The JSON files are "
   "shared between threads. Without the lock, two requests could try to "
   "write at the same time and corrupt the file. RLock also lets the same "
   "thread acquire the lock twice (for example, save inside load), which a "
   "plain Lock would not allow.")

page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# 4. p2p.py
# ═══════════════════════════════════════════════════════════════════════════════
h1("4. p2p.py — Talking to Other Nodes")

h2("Purpose")
body(
    "This file is how a node talks to other nodes. It does four things: "
    "announce ourselves to a peer, fetch a peer's chain or organization list, "
    "broadcast a new transaction to every peer, and resolve consensus by "
    "adopting the longest valid chain.")

h2("Libraries Used")
bullet("requests — a small, popular HTTP client that makes web requests in one line of code.")

h2("Top-of-File Constant")
code("REQ_TIMEOUT = 3.0")
body(
    "Every HTTP call uses a 3-second timeout. If a peer is offline, the call "
    "returns within 3 seconds rather than hanging the app. This is essential "
    "in a peer-to-peer system where peers join and leave freely.")

h2("The Five Functions")

h3("fetch_chain(peer_url)")
body(
    "Sends GET /api/chain to the peer and returns the chain. If the peer is "
    "unreachable, returns None. The try/except is what makes the network "
    "resilient — a node never crashes because a peer is down.")

h3("fetch_orgs(peer_url)")
body(
    "Same pattern, but for the organization registry. The remote endpoint "
    "strips private keys before responding, so this call only returns public "
    "material.")

h3("announce_to_peer(peer_url, self_url)")
body(
    "POSTs our public URL to the peer's /api/peers/register. The peer adds "
    "us to its peer list. After this call, both nodes know about each other.")

h3("broadcast_tx(peers, tx)")
body(
    "Walks the peer list and sends a POST with the new transaction to each "
    "peer's /api/threats/receive. Counts how many accepted. Peers that "
    "time out or error are skipped — the function never raises.")

h3("resolve_consensus(blockchain, peers, merge_orgs_cb)")
body(
    "Implements the longest-valid-chain rule. Loops over every peer, "
    "downloads its chain, and asks the local Blockchain.replace_chain whether "
    "to adopt it. The chain is only adopted if it is strictly longer and "
    "fully valid. merge_orgs_cb is a callback provided by app.py — it merges "
    "the peer's organization registry into the local one, so the local node "
    "has every public key it needs to verify signatures in the new chain.")

h2("Defense Q&A")
qa("Why HTTP and not a custom binary protocol?",
   "HTTP is everywhere, easy to test (curl, browser), and easy to secure with "
   "TLS later. The performance overhead is tiny for chains exchanged once "
   "every few seconds. A binary protocol would be faster but would mean "
   "writing both ends ourselves, which adds work for no real benefit at "
   "this scale.")
qa("What happens during a network split?",
   "Both sides keep mining their own blocks. When the network heals, the "
   "next consensus sync picks the longer chain. Transactions that exist only "
   "on the shorter chain are lost — this is the classic Bitcoin behaviour and "
   "is acceptable here because the same threats can be resubmitted.")
qa("Could someone inject a fake chain through this protocol?",
   "No. is_valid runs on every block of the incoming chain before "
   "replace_chain accepts it. A forged block would fail one of the three "
   "checks (signature, proof-of-work, previous-hash) and the swap would be "
   "refused. The attacker would need real private keys for the originating "
   "organizations, which they do not have.")

page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# 5. app.py
# ═══════════════════════════════════════════════════════════════════════════════
h1("5. app.py — The Flask Web Application")

h2("Purpose")
body(
    "This is the file you actually run. It builds the Flask app, defines every "
    "page (the URLs you visit in the browser) and every API endpoint (the URLs "
    "peer nodes call), and connects all the other modules together.")

h2("Libraries Used")
bullet("argparse — reads command-line flags like --node, --port, --peer.")
bullet("secrets — picks a random secret key for Flask sessions.")
bullet("threading — runs the background peer-announce task at startup.")
bullet("pathlib — for file paths.")
bullet("Flask and friends (render_template, request, session, redirect, url_for, jsonify, flash, abort, Response) — the building blocks of the web framework.")
bullet("blockchain, crypto_utils, mitigations, pdf_report, storage, p2p — the local modules above.")

h2("The create_app Factory")
body(
    "Instead of declaring the Flask app at the top of the file, we wrap it in "
    "a function called create_app. This pattern lets us start many independent "
    "node instances side by side (different names, different ports) without "
    "them stepping on each other. Each call to create_app returns a fresh "
    "Flask object with its own Blockchain and its own NodeStore.")

h3("Helpers inside create_app")
bullet("current_org() — looks up the organization fingerprint in the user's session and returns the matching registry entry. Returns None if no one is logged in.")
bullet("merge_orgs(remote_orgs) — when we adopt a peer's chain, we also merge in their organization registry so we can verify their signatures. Private keys are always stripped.")

h2("Page Routes")
body(
    "Each route is a Python function with @app.route on top. Flask calls the "
    "function when someone visits the matching URL and sends the return value "
    "back to the browser. The page routes are:")
bullet("GET / — the landing page.")
bullet("GET/POST /register — show the registration form or process it.")
bullet("GET/POST /login — pick which registered organization to act as.")
bullet("GET /logout — clear the session.")
bullet("GET /dashboard — the live threat feed (latest 50).")
bullet("GET/POST /dashboard/submit — submit a threat: sign, mine, broadcast.")
bullet("GET /dashboard/explorer — show every block with its hash and contents.")
bullet("GET/POST /dashboard/network — manage peers, trigger consensus sync.")
bullet("GET /dashboard/search — search the chain.")
bullet("GET /threats/<id>/report.pdf — download a per-threat PDF.")

h2("API Routes")
body(
    "API routes use /api/ and speak JSON instead of HTML. These are the "
    "endpoints peer nodes call:")
bullet("GET /api/chain — full chain as JSON.")
bullet("GET /api/threats — flat list of threats.")
bullet("GET /api/stats — summary numbers.")
bullet("GET /api/orgs — public organization registry (no private keys).")
bullet("POST /api/threats/receive — accept a gossiped transaction.")
bullet("POST /api/peers/register — accept a peer announcement.")
bullet("GET /api/peers — list of peer URLs.")
bullet("POST /api/sync — trigger consensus.")

h2("Glue Code")
bullet("@app.template_filter('timestamp') — formats a Unix timestamp into a readable date. Used in templates as {{ tx.timestamp | timestamp }}.")
bullet("@app.context_processor — makes the MITIGATIONS dictionary and the get_playbook helper available in every template.")
bullet("def main() — the script entry point. Reads --node, --port, --peer with argparse, builds the app, starts the peer-announce thread, runs Flask.")

h2("Defense Q&A")
qa("Does every request create a new Blockchain?",
   "No. The Blockchain is created exactly once inside create_app and stored "
   "in app.config. Every request handler reads the same instance. The factory "
   "pattern just lets us run multiple node processes side by side.")
qa("What does the Flask session do?",
   "Flask sessions are signed cookies stored in the user's browser. We use "
   "them to remember which organization the user is acting as (just the "
   "fingerprint). When the browser opens /dashboard, current_org() reads the "
   "cookie and looks up the org. No password in the prototype; password login "
   "is in the future-work list.")
qa("Why are /api/* routes separate from page routes?",
   "Because they speak different formats. Pages return HTML for humans; APIs "
   "return JSON for other nodes. Keeping them under different URL prefixes "
   "makes it easy to secure or rate-limit the API independently.")
qa("How does a new transaction reach all peers?",
   "Four steps: (1) the submitting node signs the transaction; (2) it mines "
   "a new block locally and saves the chain; (3) broadcast_tx POSTs the "
   "transaction to /api/threats/receive on each peer; (4) each peer verifies "
   "the signature, accepts the transaction, mines its own next block, saves. "
   "After this, chains may differ by one block; the next consensus sync "
   "converges them.")

page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# 6. mitigations.py
# ═══════════════════════════════════════════════════════════════════════════════
h1("6. mitigations.py — The Knowledge Catalog")

h2("Purpose")
body(
    "This is the project's curated knowledge base. It holds one entry per "
    "threat type (malware, phishing, ransomware, C2, vulnerability, DDoS, and "
    "an 'other' fallback). Each entry has: a name, a short summary, eight "
    "defensive steps, three authoritative references, and three or four "
    "curated GitHub repositories with detection rules or trained models. "
    "The file is pure data, with one tiny helper function.")

h2("Libraries Used")
body("None — just plain Python.")

h2("What an Entry Looks Like")
code(
    '"phishing": {\n'
    '    "name": "Phishing",\n'
    '    "summary": "Social-engineering attempts...",\n'
    '    "steps": ["Deploy SPF, DKIM, DMARC...", ...],\n'
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
    "The same structure repeats for every threat type. Adding a new type is "
    "as easy as adding another dictionary entry — no other file changes.")

h2("The get_playbook() Helper")
code("def get_playbook(threat_type):\n"
     "    return MITIGATIONS.get((threat_type or '').lower(), MITIGATIONS['other'])")
body(
    "One line. Looks up a playbook by threat type, falling back to 'other' if "
    "the type is unknown. The fallback guarantees that every threat — even "
    "one with a custom or unknown type — gets a playbook in the PDF and on "
    "the dashboard.")

h2("Why Is This Off-Chain?")
body(
    "Defensive practices change as new tools and rules come out. Putting the "
    "catalog on the chain would mean every update has to be mined into a new "
    "block, and old versions would live forever next to the threat reports. "
    "Keeping it in source code lets us update the catalog any time with one "
    "edit. The chain's record of threats stays unchanged; only the guidance "
    "shown next to each threat updates.")

h2("Defense Q&A")
qa("Who would maintain this catalog in production?",
   "A trusted authority — a national CERT or sector regulator — would publish "
   "the catalog as a signed, versioned external feed. Each node would "
   "download and verify the latest version. This is in the future-work list "
   "as 'Signed external catalog'.")
qa("What happens if one of the GitHub links breaks?",
   "Every repository we list is a long-running, well-known project. If one "
   "ever goes offline, replacing it is a single-line edit. The dashboard and "
   "PDFs still render fine when a URL no longer works; visitors just cannot "
   "follow that one link.")
qa("Why exactly eight steps and three references per threat?",
   "Eight steps is enough to be substantive but short enough to read on "
   "one page. Three references gives one from NIST, one from MITRE, and one "
   "from CISA — the recognised triad of authoritative US-aligned guidance. "
   "Keeping the same shape across all threat types makes the PDFs easy to "
   "scan.")

page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# 7. pdf_report.py
# ═══════════════════════════════════════════════════════════════════════════════
h1("7. pdf_report.py — Per-Threat PDF Reports")

h2("Purpose")
body(
    "When someone clicks 'Download PDF' on a threat, this file builds a "
    "professional PDF on the spot. The PDF contains the threat details, "
    "the indicators, the submitter's mitigation, the standard playbook, the "
    "standard and submitter-provided detection resources, and the cryptographic "
    "proof (block index, block hash, signature) needed to verify the PDF "
    "against the chain.")

h2("Libraries Used")
bullet("io — provides BytesIO, an in-memory buffer that ReportLab writes into.")
bullet("time — for timestamp formatting.")
bullet("reportlab.lib.pagesizes.A4 — the page size.")
bullet("reportlab.lib.styles — typography presets.")
bullet("reportlab.lib.units.cm — for margins.")
bullet("reportlab.lib.enums — alignment constants (left, right, justify, center).")
bullet("reportlab.platypus — high-level layout objects: SimpleDocTemplate, Paragraph, Table, Spacer.")
bullet("reportlab.lib.colors.HexColor — for the navy / amber / rose accent colours.")

h2("Module Constants")
body(
    "Six named colours (NAVY, AMBER, ROSE, MUTED, LIGHT, DIVIDER) and a "
    "SEVERITY_COLOR mapping (critical=red, high=orange, medium=amber, "
    "low=violet) are defined at the top so they can be reused everywhere. "
    "Centralising the colours keeps the look consistent.")

h2("Helper Functions")

h3("_styles()")
body(
    "Returns a dictionary of named paragraph styles (Title, Subtitle, Eyebrow, "
    "H2, Body, Mono, Link, MetaKey, MetaVal). Each style sets a font, size, "
    "leading (line height), colour, and spacing.")

h3("_ts(value)")
body(
    "Formats a Unix timestamp as 'YYYY-MM-DD HH:MM:SS UTC'. Wrapped in "
    "try/except so a malformed timestamp falls back to an em-dash instead "
    "of crashing.")

h3("_split_mitigation(text)")
body(
    "Looks at the submitter's mitigation text. If it looks like a numbered "
    "list ('1. block IP\\n2. patch ...'), the function strips the prefixes "
    "and returns each item as its own bullet. Otherwise it returns the whole "
    "text as one paragraph. This lets the PDF render the mitigation nicely "
    "whether the submitter wrote one paragraph or eight numbered steps.")

h3("_footer(canvas, doc)")
body(
    "Draws the running footer on every page: project name on the left, page "
    "number in the centre, date on the right.")

h2("The Main Function — build_threat_report(...)")
body(
    "Takes a threat transaction, the block index and hash that sealed it, and "
    "the playbook from mitigations.py. Returns the raw PDF bytes. The document "
    "is built in six numbered sections:")
bullet("Section 1 — Description. The submitter's free-text description.")
bullet("Section 2 — Indicators of Compromise. A bulleted, monospace list.")
bullet("Section 3 — Recommended Mitigation. The submitter's specific guidance (split into bullets if it looks like a list), or a fallback notice if blank.")
bullet("Section 4 — Standard Mitigation Playbook. The full playbook for the threat type: name, summary, eight steps, three authoritative references.")
bullet("Section 5 — Detection & Trained-Model Resources. Submitter-provided URLs plus the curated standard catalog — the section is never empty.")
bullet("Section 6 — Cryptographic Provenance. A small table with threat ID, submitter, block index, block hash, timestamp, and the first 48 characters of the signature.")
body(
    "A closing italic paragraph reminds the reader that the PDF can be "
    "re-verified against the chain by anyone who holds the submitter's "
    "public key.")

h2("Defense Q&A")
qa("How is the PDF linked to the chain?",
   "Section 6 contains the block hash and the first 48 characters of the "
   "signature, plus the threat's UUID. Anyone reading the PDF can fetch the "
   "original transaction from /api/chain on any node, recompute the canonical "
   "bytes, and re-verify the signature with the submitter's public key. If "
   "the PDF was altered, the signature on the chain still belongs to the "
   "original content, and the change is detectable.")
qa("Why ReportLab and not WeasyPrint or browser-rendered PDF?",
   "ReportLab is pure Python — no extra system libraries, no headless "
   "browser, no system fonts to install. WeasyPrint would render nicer CSS "
   "but requires GTK/Pango. For a single-file Windows install, ReportLab is "
   "the simpler choice.")
qa("Will the PDF become slow with long threat reports?",
   "In practice no. The free-text fields are short. PDF generation takes "
   "under 100 milliseconds on normal hardware. Even with thousands of "
   "indicators in one report, the PDF would still finish in under a second.")

page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# CLOSING
# ═══════════════════════════════════════════════════════════════════════════════
h1("Closing — Five Answers to Memorize")

body(
    "If you only learn five things from this book before walking into the "
    "defense, make them these.")

h3("1. Why is the chain tamper-evident?")
body(
    "Every block's hash is the SHA-256 of its content. If you change one byte "
    "of block 5, its hash changes, which breaks the previous_hash inside "
    "block 6, which breaks block 7, and so on. Every node runs is_valid and "
    "rejects the broken chain.")

h3("2. Why use RSA-PSS for signing?")
body(
    "Because it is the modern, probabilistic, formally-proven scheme that "
    "NIST FIPS 186-5 recommends. It produces a fresh random signature every "
    "time and is preferred over the older PKCS#1 v1.5.")

h3("3. Why Proof-of-Work in the prototype but Proof-of-Authority in production?")
body(
    "Proof-of-Work is visible and concrete — perfect for the demo. In a "
    "permissioned network of verified organizations (Jordan CERT, banks), "
    "Proof-of-Authority is correct: no mining, fast block times, no energy "
    "waste. The rest of the architecture is unchanged.")

h3("4. What happens to a corrupted node?")
body(
    "is_valid spots the corruption right away. The Network tab's 'Trigger "
    "Consensus Sync' fetches each peer's chain; the longest valid one (the "
    "honest chain) replaces the broken local copy. That is the tamper-recovery "
    "demo in action.")

h3("5. Why is the playbook off-chain but the threat on-chain?")
body(
    "Threats are evidence and must be permanent, signed, and unchangeable — "
    "a perfect fit for a blockchain. Mitigation playbooks evolve as defensive "
    "practices change; they must be updatable. Keeping them in a versioned "
    "Python module gives both: the on-chain record stays immutable, and the "
    "defensive guidance shown alongside it is always current.")

DOC.save(OUTPUT)
print(f"Wrote: {OUTPUT}")
