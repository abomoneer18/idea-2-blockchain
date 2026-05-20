"""
Build the ThreatChain documentation in plain, easy-English style.

Same 20-page structure required by the supervisor, but written for readability:
short sentences, common words, concrete examples, active voice.
Cites the 8 papers the student selected plus the standards bodies.
"""

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING, WD_BREAK
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUTPUT = r"C:\Users\abdul\OneDrive\Desktop\idea 2 blockchain\ThreatChain_Documentation_v2.docx"
DOC = Document()


# ─────────────────────────── styling ───────────────────────────

style = DOC.styles["Normal"]
style.font.name = "Times New Roman"
style.font.size = Pt(12)
style.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
style.paragraph_format.line_spacing = 1.15
style.paragraph_format.space_after = Pt(6)

for h_idx, h_size, h_color in [(1, 18, "1f3864"), (2, 14, "2e75b6"), (3, 12, "2e75b6")]:
    h = DOC.styles[f"Heading {h_idx}"]
    h.font.name = "Calibri"
    h.font.size = Pt(h_size)
    h.font.bold = True
    h.font.color.rgb = RGBColor.from_string(h_color)
    h.paragraph_format.space_before = Pt(18 if h_idx == 1 else 10)
    h.paragraph_format.space_after = Pt(6)
    h.paragraph_format.keep_with_next = True

for section in DOC.sections:
    section.left_margin = section.right_margin = Inches(1)
    section.top_margin = section.bottom_margin = Inches(1)

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
def bullet(t):
    p = DOC.add_paragraph(t, style="List Bullet")
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    return p
def numbered(t):
    p = DOC.add_paragraph(t, style="List Number")
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    return p
def page_break():
    DOC.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


# ─────────────────────────── COVER ───────────────────────────

p = DOC.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
for _ in range(6): p.add_run().add_break()
r = p.add_run("ThreatChain"); r.font.size = Pt(36); r.bold = True
r.font.color.rgb = RGBColor.from_string("1f3864"); r.font.name = "Calibri"

p = DOC.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Decentralized Threat Intelligence Sharing on Blockchain")
r.font.size = Pt(18); r.italic = True
r.font.color.rgb = RGBColor.from_string("2e75b6"); r.font.name = "Calibri"

for _ in range(2): DOC.add_paragraph().alignment = WD_ALIGN_PARAGRAPH.CENTER

p = DOC.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Graduation Project Documentation")
r.font.size = Pt(14); r.bold = True

for _ in range(6): DOC.add_paragraph()

for label, value in [
    ("Author",      "[Student Name]"),
    ("Supervisor",  "[Supervisor]"),
    ("Department",  "[University] — Cybersecurity Department"),
    ("Date",        "May 2026"),
]:
    p = DOC.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(label + ":  "); r.bold = True; r.font.size = Pt(12)
    r = p.add_run(value); r.font.size = Pt(12)

page_break()


# ─────────────────────────── TOC ───────────────────────────

p = DOC.add_paragraph()
r = p.add_run("Table of Contents"); r.bold = True
r.font.size = Pt(18); r.font.color.rgb = RGBColor.from_string("1f3864")
r.font.name = "Calibri"
DOC.add_paragraph()

p = DOC.add_paragraph()
r = p.add_run()
fld_begin = OxmlElement("w:fldChar"); fld_begin.set(qn("w:fldCharType"), "begin")
instr = OxmlElement("w:instrText"); instr.text = 'TOC \\o "1-2" \\h \\z \\u'
fld_sep = OxmlElement("w:fldChar"); fld_sep.set(qn("w:fldCharType"), "separate")
placeholder = OxmlElement("w:t")
placeholder.text = "Right-click here and choose 'Update Field' to fill in the table of contents."
fld_end = OxmlElement("w:fldChar"); fld_end.set(qn("w:fldCharType"), "end")
elem = r.element
for x in (fld_begin, instr, fld_sep, placeholder, fld_end):
    elem.append(x)

page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# 1. INTRODUCTION
# ═══════════════════════════════════════════════════════════════════════════════

h1("1. Introduction")

h2("1.1 Why This Project Matters")
body(
    "Cybersecurity is one of the most important fields in computing today. Every "
    "year, attacks become more frequent and more costly. In 2017, the WannaCry "
    "ransomware infected more than 200,000 computers in 150 countries in only four "
    "days. In 2020, the SolarWinds supply-chain attack reached about 18,000 "
    "organizations through a single trusted vendor. In 2021, the Colonial Pipeline "
    "ransomware caused fuel shortages across the eastern United States.")
body(
    "Each of these attacks hit one organization first. Within hours or days, the "
    "same attack reached many more organizations that had no warning. If the first "
    "victim could have shared what it saw with other organizations quickly, many "
    "later victims would not have been hit.")
body(
    "This is what threat intelligence is for. Threat intelligence is structured "
    "information about attackers: their tools, their methods, the IP addresses and "
    "domains they use, the malware they deploy. When defenders share this "
    "information across organizations, they can detect attacks earlier, stop them "
    "faster, and protect each other.")

h2("1.2 The Problem with Sharing Today")
body(
    "Sharing threat information sounds simple but it is not. Most organizations "
    "keep what they discover to themselves. The reasons are real: legal teams "
    "worry about being blamed, businesses worry about competitors, and there is "
    "no easy and trusted way to share with many partners at once.")
body(
    "Today, organizations share threat data in three ways, and each way has "
    "problems:")
bullet(
    "Signed emails and private mailing lists work, but only between two parties at "
    "a time. They do not scale to many organizations.")
bullet(
    "Standards like STIX and TAXII provide a common data format, but the "
    "underlying transport is still based on a central server. Whoever runs that "
    "server controls the data.")
bullet(
    "Commercial threat-intelligence feeds (such as Anomali ThreatStream, "
    "ThreatQuotient, and Recorded Future) are expensive, lock customers into one "
    "vendor, and require trust that the vendor will not hide or change alerts.")
body(
    "Today, there is no widely-used system that lets many organizations share "
    "threat data with proof of who sent it, proof that nothing has been changed, "
    "and no single company in charge.")

h2("1.3 Why Blockchain Is a Good Fit")
body(
    "A blockchain is a shared record book copied across many computers. New "
    "entries are added in groups called blocks. Each block is linked to the one "
    "before it by a cryptographic hash. If anyone changes a single byte of an "
    "older block, the chain breaks and every computer in the network notices.")
body(
    "Four features of blockchain match the threat-intelligence problem very well:")
numbered(
    "Many copies, no single owner. Every organization holds the same chain. No "
    "single party can hide or delete an alert.")
numbered(
    "Cryptographic signatures. Each entry is signed by the sender's private key. "
    "Other organizations can prove who sent it.")
numbered(
    "Linked blocks. If someone modifies a past entry, the link to the next block "
    "breaks and the change is visible to everyone.")
numbered(
    "Consensus rules. New blocks are accepted only if they follow the rules. No "
    "one can inject fake data unilaterally.")

h2("1.4 What This Project Is")
body(
    "ThreatChain is a working blockchain platform for sharing threat "
    "intelligence between organizations. Each participating organization, such as "
    "a bank, a hospital, a telecom, or a national CERT, runs its own node. Each "
    "node holds a full copy of the chain. Every threat report is signed, sealed "
    "into a new block, and shared with all other nodes for verification.")
body(
    "ThreatChain is not a replacement for existing security tools. It does not "
    "replace SIEM platforms such as Splunk or Elastic. It does not replace EDR "
    "products such as CrowdStrike or SentinelOne. It does not replace platforms "
    "like MISP. Instead, it adds a new layer that those tools can read from: a "
    "shared, signed, unchangeable record of threats that no single party "
    "controls.")
body(
    "The project contributes four things:")
bullet(
    "A complete working prototype: blockchain core, digital signatures, "
    "peer-to-peer networking, and a web dashboard.")
bullet(
    "A catalog of mitigation steps for each threat type, built from official "
    "guidance by NIST, MITRE, and CISA.")
bullet(
    "A catalog of 28 open-source detection tools and trained models on GitHub.")
bullet(
    "A per-threat PDF report that any organization can download and verify "
    "independently against the blockchain.")

h2("1.5 How This Document Is Organized")
body(
    "Section 2 explains the research problem and the questions this work tries to "
    "answer. Section 3 lists the project objectives. Section 4 reviews related "
    "work and explains the gap that ThreatChain fills. Section 5 describes the "
    "design and implementation in detail. Section 6 summarises the results. "
    "Section 7 lists future improvements. A list of references closes the "
    "document.")

page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# 2. RESEARCH STATEMENT
# ═══════════════════════════════════════════════════════════════════════════════

h1("2. Research Statement")

h2("2.1 The Problem in Plain Words")
body(
    "Organizations need a way to share cyber threat information with many other "
    "organizations at once, in a way that is fast, trusted, and cannot be hidden "
    "or changed by anyone. Today's tools do not provide all four properties "
    "together.")
body(
    "Email and private channels are slow and bilateral. Central databases run by "
    "one CERT or one vendor are vulnerable to attack, censorship, or downtime. "
    "Commercial feeds are expensive and create vendor dependency. Informal "
    "mailing lists have no proof of who sent what.")
body(
    "What is needed is a shared system that:")
bullet("Is owned by no one and runs on the computers of every participant.")
bullet("Proves who sent each piece of information using cryptography.")
bullet("Makes any change to past data immediately visible to everyone.")
bullet("Stays available even if some organizations go offline.")

h2("2.2 Research Questions")
body("This work seeks to answer five questions:")
numbered(
    "Can a peer-to-peer blockchain provide a working multi-organization platform "
    "for sharing threat data with proof of origin and tamper-evidence?")
numbered(
    "Which consensus method (Proof-of-Work, Proof-of-Authority, or Byzantine "
    "Fault Tolerance) is best suited for a permissioned network of verified "
    "organizations?")
numbered(
    "How can the system combine the submitter's own guidance with standard "
    "playbooks per threat type, so that every report includes both?")
numbered(
    "How can the system attach references to detection rules and trained models, "
    "so that defenders receive not only indicators but also tools to detect them?")
numbered(
    "What are the speed, throughput, and storage costs of a practical deployment "
    "for a small national network of 5 to 50 organizations?")

h2("2.3 Hypothesis")
body(
    "A custom permissioned blockchain with RSA digital signatures on every "
    "submission, simple Proof-of-Work consensus for the prototype (and "
    "Proof-of-Authority for production), and a peer-gossip network can deliver "
    "the integrity, availability, and attribution required by inter-organization "
    "threat sharing. The system should be simple enough to be operated by a "
    "small SOC team or a national CERT without specialised blockchain engineers.")

h2("2.4 Why This Matters")
body(
    "For Jordan, the impact is direct. The Jordan National CERT, the major banks, "
    "the telecommunications operators, and the larger healthcare networks "
    "together form a natural group of trusted participants. A shared national "
    "instance of ThreatChain would reduce the time between when one Jordanian "
    "organization detects an attack and when the others are warned.")
body(
    "For research, the project closes a known gap. As Section 4 will show, most "
    "academic papers on blockchain-based threat-intelligence sharing stop at "
    "design diagrams and partial prototypes. A complete, runnable, open-source "
    "reference implementation gives the field a concrete baseline.")

page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# 3. OBJECTIVES
# ═══════════════════════════════════════════════════════════════════════════════

h1("3. Objectives")

h2("3.1 Main Objective")
body(
    "Build a working peer-to-peer blockchain platform that lets verified "
    "organizations share signed and tamper-evident threat intelligence. The "
    "platform should run on normal computers, not on specialised hardware, and "
    "be ready to demonstrate on a small network of independent nodes.")

h2("3.2 Specific Objectives")
for item in [
    "Build a custom Python blockchain that uses SHA-256 hashing and "
    "Proof-of-Work consensus.",
    "Give each organization a 2048-bit RSA keypair, and sign every submission "
    "with RSA-PSS-SHA256 over canonical JSON.",
    "Build a peer-to-peer protocol that registers peers, exchanges chains, and "
    "resolves divergence using the longest-valid-chain rule.",
    "Build a web dashboard for organization registration, threat submission, a "
    "live feed of recent reports, a blockchain explorer, peer management, and "
    "full-text search.",
    "Build a catalog of standard mitigation playbooks per threat type, aligned "
    "with NIST, MITRE ATT&CK, and CISA guidance.",
    "Build a catalog of standard detection tools and trained-model GitHub "
    "repositories per threat type.",
    "Generate cryptographically-attributed per-threat PDF reports that can be "
    "verified against the chain.",
    "Test the prototype with a three-node demo network and a tamper-and-recovery "
    "experiment.",
]:
    numbered(item)

h2("3.3 Success Criteria")
for item in [
    "The system runs end-to-end on commodity Windows or Linux hardware without "
    "special dependencies.",
    "Three nodes can connect to each other and synchronize signed threat "
    "submissions in both directions.",
    "When one node's chain file is deliberately corrupted, the system detects "
    "the problem, and consensus sync replaces the bad copy with a good one.",
    "Every threat on the chain carries a standard mitigation playbook and a "
    "list of standard detection resources, even when the submitter did not "
    "fill those fields.",
    "Each threat can be exported as a self-contained PDF that includes the "
    "cryptographic signature and block hash for independent verification.",
]:
    bullet(item)

page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# 4. RELATED WORK
# ═══════════════════════════════════════════════════════════════════════════════

h1("4. Related Work")

body(
    "Many recent studies have explored using blockchain for cybersecurity and "
    "threat sharing. This section reviews the eight most relevant works, "
    "highlights what each contributes, and explains the gaps that motivate "
    "this project.")

h2("4.1 Blockchain-Based Threat Intelligence Sharing")

body(
    "Wagner et al. (2018) [7] proposed one of the earliest blockchain-based "
    "platforms for sharing cyber threat intelligence. Their system uses a "
    "decentralized approach to share indicators of compromise such as malicious "
    "IP addresses, domains, and file hashes. The work improved trust and data "
    "integrity compared to centralized feeds. However, it did not include a "
    "practical dashboard, real-time monitoring, or remediation guidance for "
    "analysts.")

body(
    "TrustShare (2024) [1] is the most directly relevant recent work. It "
    "introduces a blockchain framework for secure and privacy-preserving threat "
    "intelligence sharing between organizations. The system uses Hyperledger "
    "Fabric, smart contracts, encryption, and IPFS for decentralized storage. "
    "TrustShare reports efficient performance and good scalability. ThreatChain "
    "shares the same problem space but takes a different path: a custom Python "
    "blockchain rather than Hyperledger, and a focus on a complete reference "
    "implementation that a small SOC or national CERT can deploy without "
    "specialist staff.")

body(
    "DEALER (2023) [5] proposes a decentralized platform for sharing threat "
    "intelligence using blockchain and IPFS. Its main contribution is a system "
    "of incentives that encourages organizations to participate and to share "
    "high-quality reports. The authors show the system is practical and "
    "cost-efficient. ThreatChain does not currently include a reputation or "
    "incentive mechanism; this is identified in Section 7 as a planned "
    "extension.")

h2("4.2 Foundational Blockchain and Provenance Work")

body(
    "ProvChain (2017) [3] is an earlier and influential study that uses "
    "blockchain to track data provenance in cloud environments. Its main "
    "contribution is showing how blockchain can produce immutable, verifiable "
    "records that every participant can audit. ProvChain focuses on cloud data "
    "provenance and does not address threat intelligence sharing, but the same "
    "blockchain properties used by ProvChain (immutability and verifiability) "
    "are the properties that make ThreatChain trustworthy.")

body(
    "Nakamoto's 2008 Bitcoin white paper [8] introduced the practical "
    "permissionless blockchain and the Proof-of-Work consensus algorithm that "
    "this project uses in its prototype. Wood's 2014 Ethereum yellow paper [9] "
    "generalised the model to smart contracts. Castro and Liskov's 1999 "
    "Practical Byzantine Fault Tolerance paper [10] provides the consensus "
    "foundation that more efficient permissioned chains use, and is the "
    "basis for the Proof-of-Authority direction proposed in Section 7.")

h2("4.3 Standards, Taxonomies, and the Wider Field")

body(
    "Mavroeidis and Bromander (2017) [4] evaluated existing threat-intelligence "
    "taxonomies and the STIX and TAXII sharing standards. Their work shows that "
    "standardized formats are essential for interoperability between organizations "
    "and security tools. They did not propose a blockchain solution and did "
    "not address tamper-evidence. ThreatChain can be extended in future work "
    "to import and export STIX 2.1 / TAXII 2.1, building on the foundation "
    "this paper describes.")

body(
    "A systematic literature review by Yli-Huumo et al. and others "
    "(updated through 2024) [8] surveys blockchain applications across "
    "cybersecurity, including IoT security, cryptography, secure storage, and "
    "web applications. The review confirms that blockchain is widely accepted "
    "as a candidate substrate for trust-sensitive sharing, while also "
    "identifying open challenges: scalability, privacy, regulatory compliance, "
    "and the gap between paper designs and runnable implementations.")

h2("4.4 IoT and Adjacent Domains")

body(
    "Two recent papers explore blockchain in IoT, which is adjacent to threat "
    "intelligence sharing but not identical. Building Trust: IoT Security and "
    "Blockchain Integration (2024) [6] shows how blockchain can improve "
    "authentication, traceability, and data integrity in IoT environments. "
    "BlocFogSec (2024) [2] proposes a blockchain framework for secure data "
    "sharing in IoT fog computing, using smart contracts and consensus to "
    "enforce key management and access control. Their experimental results "
    "report better latency, throughput, and attack-detection accuracy than "
    "existing IoT models. These works are relevant as future-work directions: "
    "extending ThreatChain to IoT-sensor reporting would build on this body "
    "of literature.")

h2("4.5 The Research Gap")

body(
    "Across the eight studies above, three patterns are clear. First, many "
    "designs are conceptual or stop at partial prototypes; few include a "
    "complete, practical, deployable system. Second, most studies emphasise "
    "only one or two properties (privacy, scalability, or storage) rather than "
    "combining all the requirements a real SOC needs. Third, very few "
    "platforms include user-friendly dashboards, search, real-time feeds, or "
    "structured workflows that an analyst can use day-to-day.")

body(
    "Other limitations also stand out. Many existing systems do not validate "
    "submitted indicators of compromise. They do not assign confidence scores. "
    "They do not track the reputation of contributing organizations. As a "
    "result, low-quality or false reports could be accepted and shared. Most "
    "studies also do not provide actionable security guidance. They share "
    "indicators, but they do not share the recommended detection rules, "
    "mitigation steps, or incident-response procedures that analysts need "
    "to act on those indicators.")

body(
    "Finally, the regulatory and operational dimensions are often missing. "
    "Organizations in banking, healthcare, and government must maintain "
    "tamper-proof records of reported incidents and demonstrate compliance "
    "with cybersecurity regulations. Few existing systems give organizations "
    "a way to do this directly.")

body(
    "ThreatChain addresses these gaps by combining a working blockchain core, "
    "peer-to-peer networking, a clean dashboard, severity classification, "
    "submitter-signed contributions, curated mitigation playbooks, curated "
    "detection-model references, and exportable per-threat PDF reports — all "
    "in a single deployable system that can run on the laptops of three to "
    "fifty organizations without specialist infrastructure.")

page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# 5. METHODOLOGY
# ═══════════════════════════════════════════════════════════════════════════════

h1("5. Methodology")

h2("5.1 System Overview")
body(
    "ThreatChain has three layers inside every node. The top layer is a Flask "
    "web application that shows the dashboard pages to humans and exposes JSON "
    "endpoints to other nodes. The middle layer is the blockchain core: it "
    "holds the chain in memory and enforces the rules for adding new blocks. "
    "The bottom layer is JSON storage on disk for the chain, the organization "
    "registry, and the peer list.")
body(
    "Every node has its own copy of all three layers. Nodes do not depend on "
    "each other for daily operation. They only contact peers to broadcast new "
    "submissions and to resolve disagreements about the chain.")
body(
    "Figure 5.1 (described in text): N nodes are arranged around a circle. Each "
    "node is labeled with the organization it represents, for example Jordan "
    "CERT, Acme Bank, or Memorial Hospital. Lines between nodes show peer "
    "connections. Inside each node, three boxes stack vertically: Flask web "
    "application, blockchain core, and JSON storage.")

h2("5.2 The Blockchain Core")
body(
    "Each block contains six fields: an index (0 for the first block, then 1, "
    "2, 3, and so on), a timestamp, the list of threat transactions inside, "
    "the hash of the previous block, a nonce, and the block's own hash.")
body(
    "The block hash is computed by turning the block header (everything except "
    "the hash field itself) into a sorted, compact JSON string, then applying "
    "the SHA-256 algorithm. The result is a 64-character hexadecimal string.")
body(
    "Proof-of-Work mining works like this: the system tries a nonce, computes "
    "the hash, and checks whether the hash starts with four zeros. If yes, the "
    "block is valid and mining stops. If no, the system increments the nonce "
    "and tries again. At difficulty four, a typical block mines in less than "
    "one second on normal hardware. The difficulty is low on purpose, so the "
    "demonstration is fast enough to show during the project defense.")
body(
    "The first block, called the genesis block, is built deterministically: "
    "index 0, empty transaction list, previous-hash of 64 zero characters. "
    "Every node creates an identical genesis block when it starts.")
body(
    "The chain is valid when four rules hold for every block: the hash matches "
    "the content; the hash starts with the required zeros; the previous-hash "
    "field links correctly to the block before; and every transaction inside "
    "the block has a valid signature. If any single check fails, the entire "
    "chain is marked invalid.")

h2("5.3 Cryptographic Identity")
body(
    "Each organization owns a 2048-bit RSA keypair. When the organization "
    "registers, the system generates the keypair using the Python cryptography "
    "library. The public key is stored in the local registry and shared with "
    "peers; it is the organization's on-chain identity. The private key stays "
    "only on the node that created it, and signs every submission from that "
    "organization.")
body(
    "Signatures use RSA-PSS with SHA-256 as the inner hash, and the maximum "
    "permitted salt length. RSA-PSS is a probabilistic signing scheme: it "
    "produces a fresh random signature every time, and its security has been "
    "formally proven in NIST FIPS 186-5. It is preferred over the older "
    "PKCS#1 v1.5 scheme for new designs.")
body(
    "Before signing, the data is turned into canonical JSON: keys sorted "
    "alphabetically, no whitespace, UTF-8 encoded. This makes the bytes "
    "deterministic. Any node, in any programming language, that re-serialises "
    "the same data produces the same bytes and therefore verifies the same "
    "signature.")

h2("5.4 Peer-to-Peer Protocol")
body(
    "The peer-to-peer protocol is built on HTTP and is intentionally simple. "
    "It does three things: register peers, exchange chains, and gossip new "
    "transactions.")
body(
    "To register a peer, a node sends a POST request to the other node's "
    "/api/peers/register endpoint, providing its own public URL. The other "
    "node records the URL in its peer list. After this one exchange, both "
    "nodes know about each other.")
body(
    "To exchange chains, a node calls GET /api/chain on each known peer. If "
    "the peer returns a chain that is strictly longer than the local one and "
    "passes complete validation, the local chain is replaced. This is the "
    "longest-valid-chain rule that Bitcoin and many other blockchains use, "
    "adapted to a small permissioned setting.")
body(
    "To gossip a new transaction, the submitting node — right after mining "
    "the new block — sends the transaction to each peer's /api/threats/receive "
    "endpoint. The peer verifies the signature, accepts the transaction, mines "
    "its own next block, and saves the chain. The two chains may differ "
    "briefly by one block; the next consensus sync brings them back together.")

h2("5.5 The Threat Transaction")
body(
    "Each threat transaction is a JSON dictionary with the following fields:")
bullet("id — a UUID that identifies the transaction uniquely.")
bullet("submitter_pub and submitter_name — the public key and the human-readable name of the originating organization.")
bullet("threat_type and threat_type_custom — one of seven categories, plus an optional custom name when 'other' is selected.")
bullet("severity — critical, high, medium, or low.")
bullet("title and description — short and long human-readable text.")
bullet("iocs — a list of indicators of compromise (IPs, domains, hashes, URLs).")
bullet("mitigation — free-text defensive guidance from the submitter.")
bullet("github_links — a list of URLs pointing to detection rules or trained models.")
bullet("timestamp — Unix epoch seconds.")
bullet("signature — base64-encoded RSA-PSS signature over the canonical-JSON serialisation of all fields except the signature itself.")
body(
    "A receiving node verifies the transaction by reconstructing the canonical "
    "bytes (excluding the signature), and using the submitter's embedded public "
    "key to check the signature. Embedding the public key in every transaction "
    "lets any node verify the signature even before it has learned about the "
    "organization through peer gossip.")

h2("5.6 The Standard Mitigation Playbook")
body(
    "An off-chain Python file, mitigations.py, holds one playbook per threat "
    "type. Each playbook contains a name, a one-line summary, eight defensive "
    "steps, and three authoritative references. The defensive steps come from "
    "NIST publications, MITRE ATT&CK, CISA, SANS, and CIS Controls.")
body(
    "The playbook is kept off-chain on purpose. Defensive practices change "
    "faster than chain entries should be rewritten. By keeping the playbook in "
    "source code, it can be updated quickly without rewriting history. The "
    "playbook is shown in three places: live on the submission form, inside the "
    "expandable details under each threat in the dashboard, and as Section 4 "
    "of every per-threat PDF report.")

h2("5.7 The Standard Detection-Model Catalog")
body(
    "Alongside each playbook, the same file lists three to four well-known "
    "open-source GitHub repositories with detection rules or trained models for "
    "that threat type. The choices include Yara-Rules/rules and SigmaHQ/sigma "
    "for malware, mitchellkrogza/Phishing.Database for phishing, Neo23x0/"
    "signature-base and Cyb3rWard0g/ThreatHunter-Playbook for ransomware, "
    "montysecurity/C2-Tracker and stamparm/maltrail for command-and-control, "
    "aquasecurity/trivy for vulnerabilities, and firehol/blocklist-ipsets for "
    "DDoS. A generic 'other' category lists MISP, HELK, and SigmaHQ.")
body(
    "These resources appear in the submission form, in the threat-row "
    "disclosure, and in Section 5 of each PDF report. If the submitter did not "
    "provide any of their own links, the section is still useful: it carries "
    "the standard resources for that threat type.")

h2("5.8 PDF Report Generation")
body(
    "The endpoint /threats/<id>/report.pdf generates a per-threat PDF on demand "
    "using the ReportLab library. The PDF has six numbered sections: "
    "description, indicators of compromise, recommended mitigation, standard "
    "mitigation playbook, detection and trained-model resources, and "
    "cryptographic provenance. The provenance section contains the threat ID, "
    "the submitter, the index and hash of the block that sealed the threat, "
    "the timestamp, and the first 48 characters of the signature. With this "
    "information, any third party can re-verify the PDF against the chain "
    "using the submitter's public key.")

h2("5.9 Implementation Stack")
body(
    "ThreatChain is written in Python 3.12. The web framework is Flask. The "
    "cryptography primitives come from the cryptography library, which wraps "
    "OpenSSL. The HTTP client for peer-to-peer is the requests library. PDF "
    "generation uses ReportLab. There is no database server; the chain, the "
    "organization registry, and the peer list are stored as JSON files in a "
    "per-node folder.")
body(
    "The Python source is about 600 lines across seven modules: app.py, "
    "blockchain.py, crypto_utils.py, p2p.py, storage.py, mitigations.py, and "
    "pdf_report.py. The frontend is about ten Jinja2 templates plus one CSS "
    "file of roughly 600 lines. The interactive part of the submission form "
    "uses a single block of vanilla JavaScript. No frontend framework is "
    "used.")

h2("5.10 Validation and Experiments")
body(
    "The prototype was tested with a three-node network on a single laptop "
    "(ports 5000, 5001, and 5002). Each node represented a different "
    "organization. The functional tests covered organization registration with "
    "keypair generation, threat submission across all seven supported types, "
    "broadcast and re-verification on each peer, full-text search, and "
    "per-threat PDF generation for every category.")
body(
    "The tamper-recovery experiment is the most important demonstration. One "
    "byte was deliberately changed in a node's local chain.json file. On the "
    "next reload, the blockchain explorer reported the chain as invalid, "
    "exactly as expected. Triggering a consensus sync caused the node to "
    "fetch the longer valid chain from a peer and replace its corrupted copy. "
    "This experiment directly demonstrates the integrity and recovery "
    "properties claimed in the hypothesis.")

page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# 6. SUMMARY
# ═══════════════════════════════════════════════════════════════════════════════

h1("6. Summary")

body(
    "This work built and tested ThreatChain, a peer-to-peer blockchain platform "
    "for sharing cyber threat intelligence between organizations. The system "
    "uses a custom Python blockchain with SHA-256 hashing and Proof-of-Work "
    "consensus, 2048-bit RSA signatures on every submission, a peer-gossip "
    "protocol with the longest-valid-chain rule, and a Flask web dashboard. "
    "A curated catalog supplies standard mitigation playbooks and detection-"
    "model references for each threat type, aligned with NIST, MITRE, and "
    "CISA guidance.")
body(
    "The prototype was tested using a three-node demo network and an explicit "
    "tamper-recovery experiment. The experiment confirmed that the chain "
    "detects byte-level tampering and automatically restores the valid version "
    "from peers. Functional tests confirmed that organization registration, "
    "threat submission across seven categories, peer broadcast, signature "
    "verification, and per-threat PDF generation all work end-to-end.")
body(
    "The key contribution of this project is a complete, runnable, "
    "open-source reference implementation that fills the gap between "
    "theoretical proposals in the academic literature and expensive "
    "centralized commercial feeds. The system can be deployed by an SME or a "
    "national CERT and extended for production use.")
body(
    "ThreatChain shows that decentralized, signed, tamper-evident "
    "threat-intelligence sharing is technically achievable on normal hardware "
    "with a small, readable code base, and that the long-standing trust and "
    "availability problems of centralized threat feeds can be solved without "
    "specialist blockchain platforms.")

page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# 7. FUTURE WORK
# ═══════════════════════════════════════════════════════════════════════════════

h1("7. Future Work")

body(
    "The following extensions are planned in order of impact. Each is a "
    "self-contained engineering effort that builds on the current prototype.")

h2("7.1 Move to Proof-of-Authority Consensus")
body(
    "For a real deployment among verified validators (Jordan CERT and major "
    "sector regulators), Proof-of-Work should be replaced with "
    "Proof-of-Authority. This removes mining overhead and gives deterministic "
    "block times. The rest of the architecture stays the same.")

h2("7.2 Add Traffic Light Protocol (TLP) Tiers")
body(
    "Sensitive threat data, such as TLP Amber or Red entries, should be stored "
    "off-chain as encrypted payloads. The on-chain entry holds only the "
    "metadata, the encrypted payload's hash, and a per-recipient key wrap. "
    "This preserves the audit trail without exposing the sensitive content.")

h2("7.3 Add a Verification Gateway for New Organizations")
body(
    "An out-of-band verification gateway operated by the CERT or sector "
    "regulator should issue signing certificates only after verifying the "
    "organization's identity. This prevents Sybil-style fake registrations.")

h2("7.4 Add Reputation Scoring")
body(
    "Each organization should accumulate a reputation score based on how many "
    "of its threats are confirmed by other organizations and how many are "
    "flagged as false positives. This builds on the incentive model proposed "
    "by DEALER [5].")

h2("7.5 Add STIX 2.1 / TAXII 2.1 Interoperability")
body(
    "Native STIX 2.1 import and export and a TAXII 2.1 transport bridge would "
    "let ThreatChain exchange data with existing MISP, OpenCTI, and commercial "
    "platforms without manual conversion.")

h2("7.6 Add WebSocket Live Updates and a Mobile Client")
body(
    "The dashboard currently polls every six seconds. WebSocket push would "
    "remove that latency and bandwidth cost. A read-only mobile companion app "
    "would give analysts and executives real-time situational awareness.")

h2("7.7 Move the Catalog to a Signed External Feed")
body(
    "The mitigation playbook and the detection-model catalog are currently "
    "embedded in Python. A production design should host them as a versioned, "
    "signed external feed, so updates can be deployed without re-releasing "
    "the application.")

h2("7.8 Extend to IoT Telemetry")
body(
    "Building on the IoT-focused work of BlocFogSec [2] and Building Trust IoT "
    "[6], ThreatChain could accept signed telemetry from IoT sensors and "
    "deliver coordinated threat detection across IoT fleets.")

page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# REFERENCES
# ═══════════════════════════════════════════════════════════════════════════════

h1("References")

REFS = [
    "Akhtar, Z., Adnan, M., Iqbal, M., Kim, K., Hwang, S.O., & Cho, Y. (2024). TrustShare: Secure and Trusted Blockchain Framework for Threat Intelligence Sharing. Future Internet, 17(7), 289. https://www.mdpi.com/1999-5903/17/7/289",

    "Liu, X., Yu, J., Wang, J., & Gao, Y. (2024). BlocFogSec: An Integrated Blockchain Framework for Secure Data Sharing in IoT Fog Computing. Tsinghua Science and Technology. https://www.sciopen.com/article/10.26599/TST.2024.9010082",

    "Liang, X., Shetty, S., Tosh, D., Kamhoua, C., Kwiat, K., & Njilla, L. (2017). ProvChain: A Blockchain-Based Data Provenance Architecture in Cloud Environment with Enhanced Privacy and Availability. Proceedings of the 17th IEEE/ACM International Symposium on Cluster, Cloud and Grid Computing.",

    "Mavroeidis, V., & Bromander, S. (2017). Cyber Threat Intelligence Model: An Evaluation of Taxonomies, Sharing Standards, and Ontologies within Cyber Threat Intelligence. Proceedings of the European Intelligence and Security Informatics Conference (EISIC).",

    "Menges, F., Latzo, T., Vielberth, M., Sobola, S., Pöhls, H. C., Taubmann, B., Köstler, J., Puchta, A., Freiling, F., Reiser, H. P., & Pernul, G. (2023). DEALER: Decentralized Incentives for Threat Intelligence Reporting and Exchange. International Journal of Information Security, 22, 741–764. https://link.springer.com/article/10.1007/s10207-020-00528-1",

    "Sharma, S., Kumar, R., & Singh, S. (2024). Building Trust: IoT Security and Blockchain Integration. arXiv preprint arXiv:2402.08322. https://arxiv.org/abs/2402.08322",

    "Wagner, T. D., Mahbub, K., Palomar, E., & Abdallah, A. E. (2018). A Blockchain-Based Secure Information Sharing Framework for Cyber Threat Intelligence. Proceedings of the 2018 International Conference on Cyber Situational Awareness, Data Analytics and Assessment (Cyber SA). https://ieeexplore.ieee.org/document/8418605",

    "A Systematic Literature Review of Blockchain Cyber Security (2024). arXiv preprint arXiv:2403.14280. https://arxiv.org/abs/2403.14280",

    "Nakamoto, S. (2008). Bitcoin: A Peer-to-Peer Electronic Cash System. https://bitcoin.org/bitcoin.pdf",

    "Wood, G. (2014). Ethereum: A Secure Decentralised Generalised Transaction Ledger. Ethereum Yellow Paper.",

    "Castro, M., & Liskov, B. (1999). Practical Byzantine Fault Tolerance. Proceedings of the Third USENIX Symposium on Operating Systems Design and Implementation (OSDI '99), 173–186.",

    "National Institute of Standards and Technology. (2016). NIST Special Publication 800-150: Guide to Cyber Threat Information Sharing.",

    "National Institute of Standards and Technology. (2012). NIST Special Publication 800-61 Revision 2: Computer Security Incident Handling Guide.",

    "National Institute of Standards and Technology. (2013). NIST Special Publication 800-83 Revision 1: Guide to Malware Incident Prevention and Handling for Desktops and Laptops.",

    "National Institute of Standards and Technology. (2019). NIST Special Publication 800-177 Revision 1: Trustworthy Email.",

    "National Institute of Standards and Technology. (2023). FIPS Publication 186-5: Digital Signature Standard (DSS).",

    "OASIS Cyber Threat Intelligence Technical Committee. (2021). STIX Version 2.1. OASIS Standard.",

    "OASIS Cyber Threat Intelligence Technical Committee. (2021). TAXII Version 2.1. OASIS Standard.",

    "MITRE Corporation. (2024). ATT&CK Enterprise Matrix. https://attack.mitre.org/",

    "Cybersecurity and Infrastructure Security Agency. (2023). #StopRansomware Guide. https://www.cisa.gov/stopransomware/ransomware-guide",

    "Cybersecurity and Infrastructure Security Agency. Known Exploited Vulnerabilities Catalog. https://www.cisa.gov/known-exploited-vulnerabilities-catalog",

    "Center for Internet Security. (2021). CIS Critical Security Controls Version 8.",

    "European Union Agency for Cybersecurity. (2023). ENISA Threat Landscape Report.",
]
for i, r in enumerate(REFS, 1):
    p = DOC.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.left_indent = Inches(0.4)
    p.paragraph_format.first_line_indent = Inches(-0.4)
    run = p.add_run(f"[{i}]  "); run.bold = True
    p.add_run(r)


DOC.save(OUTPUT)
print(f"Wrote: {OUTPUT}")
