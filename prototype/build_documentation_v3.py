"""
Build ThreatChain documentation - v3 - natural student writing style.
Same structure and content as v2, but written the way a real student writes:
  - slightly informal in places
  - minor grammatical imperfections
  - occasional repetition of a word
  - not perfectly polished sentences
  - mixes simple and complex sentences in a believable way
  - some transitions that are a bit clunky
  - references to "I" / "we" as a student would sometimes say
"""

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING, WD_BREAK
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUTPUT = r"C:\Users\abdul\OneDrive\Desktop\idea 2 blockchain\ThreatChain_Documentation_v3.docx"
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


# ═══════════════════════════════════════════════════════════════
# 1. INTRODUCTION
# ═══════════════════════════════════════════════════════════════

h1("1. Introduction")

h2("1.1 Why This Project Is Important")
body(
    "Cybersecurity is one of the most important areas in the field of information "
    "technology today. Attacks are increasing every year, and their effects are "
    "becoming more and more serious. For example, in 2017 the WannaCry ransomware "
    "spread very quickly and infected more than 200,000 computers across 150 "
    "countries in just four days. Then in 2020, a major attack called SolarWinds "
    "happened, where attackers entered the systems of around 18,000 organizations "
    "through a single software update. And in 2021, the Colonial Pipeline attack "
    "caused fuel shortages in a large part of the United States.")
body(
    "In all of these cases, the attack hit one organization first. Then, after "
    "some hours or days, the same attack reached many other organizations that "
    "had no warning at all. If the first victim was able to share what it found "
    "with others quickly, maybe many of those other victims could have been "
    "protected.")
body(
    "This is basically what threat intelligence is. It is information about how "
    "attackers work, what tools they use, which IP addresses or domains they "
    "operate from, and what malware they use. When this kind of information is "
    "shared between organizations, it helps everyone detect attacks faster and "
    "respond better.")

h2("1.2 The Problem with How Sharing Works Today")
body(
    "Sharing threat information sounds like an easy thing to do, but in practice "
    "it is not. Most organizations do not share what they discover. There are "
    "several reasons for this. Legal departments are often worried about legal "
    "responsibility. Companies are afraid of sharing information with competitors. "
    "And there is also the simple fact that there is no easy or trusted way to "
    "share with many partners at the same time.")
body(
    "Currently, there are about three main ways that organizations share threat "
    "data, and each one has its own problems:")
bullet(
    "Signed emails and private mailing lists — these work, but only between two "
    "parties at a time and they do not work well when you have many organizations "
    "who want to share.")
bullet(
    "Standards like STIX and TAXII — these give a common data format, but they "
    "still rely on a central server. Whoever owns that server has control over "
    "all the data.")
bullet(
    "Commercial threat intelligence services like Anomali ThreatStream or "
    "Recorded Future — these are expensive, they lock organizations into one "
    "vendor, and you have to trust that vendor completely.")
body(
    "So basically, there is no widely-used system today that allows many "
    "organizations to share threat data with proof of who sent it, proof that "
    "nothing was changed, and with no single company in charge of everything.")

h2("1.3 Why Blockchain Is Suitable Here")
body(
    "A blockchain is basically a shared record book that is copied on many "
    "computers at the same time. New entries are added in groups called blocks. "
    "Each block is connected to the one before it using a cryptographic hash, "
    "which is like a digital fingerprint. If someone changes even one byte in an "
    "old block, the fingerprint changes and all computers in the network will "
    "notice that something is wrong.")
body(
    "There are four main features of blockchain that make it a good fit for this "
    "problem:")
numbered(
    "No single owner — every organization keeps a full copy of the chain, so "
    "no one can hide or delete an alert.")
numbered(
    "Digital signatures — each entry is signed with the sender's private key, "
    "so other organizations can prove who sent the information.")
numbered(
    "Linked blocks — if someone modifies an old entry, the link to the next "
    "block will break and this will be visible to everyone.")
numbered(
    "Consensus rules — new blocks are only accepted if they follow the agreed "
    "rules, so nobody can just inject fake data.")

h2("1.4 What ThreatChain Is")
body(
    "ThreatChain is a working blockchain platform that is designed for sharing "
    "threat intelligence between organizations. Each organization, for example a "
    "bank, a hospital, a telecom company, or a national CERT, runs its own node. "
    "Each node has a full copy of the blockchain. When an organization submits a "
    "new threat report, the report is digitally signed, added to a new block, "
    "and then sent to all other nodes so they can verify it.")
body(
    "ThreatChain is not meant to replace the security tools that organizations "
    "already use. It is not trying to replace SIEM platforms like Splunk or EDR "
    "products like CrowdStrike. Instead, it adds a new layer on top of those "
    "tools: a shared, signed, and tamper-proof record of threats that no single "
    "party controls.")
body(
    "The project delivers four main things:")
bullet(
    "A complete working prototype that includes the blockchain core, digital "
    "signatures, peer-to-peer networking, and a web dashboard.")
bullet(
    "A catalog of mitigation steps for each threat type, based on guidance from "
    "NIST, MITRE, and CISA.")
bullet(
    "A catalog of 28 open-source detection tools and machine learning models "
    "from GitHub.")
bullet(
    "A per-threat PDF report that any organization can download and verify "
    "by checking it against the blockchain.")

h2("1.5 Structure of This Document")
body(
    "Section 2 explains the research problem and the main questions this project "
    "tries to answer. Section 3 lists the project objectives. Section 4 reviews "
    "related work and identifies the gap that ThreatChain is trying to fill. "
    "Section 5 describes how the system was designed and built. Section 6 gives "
    "a summary of the results. Section 7 discusses future improvements. "
    "References are listed at the end.")

page_break()


# ═══════════════════════════════════════════════════════════════
# 2. RESEARCH STATEMENT
# ═══════════════════════════════════════════════════════════════

h1("2. Research Statement")

h2("2.1 The Problem")
body(
    "Organizations need a way to share cyber threat information with many other "
    "organizations at the same time, in a way that is trusted and cannot be "
    "modified or hidden by anyone. The tools that exist today do not provide all "
    "of these properties at once.")
body(
    "Email and private channels are slow and only work between two parties. "
    "Central databases that are run by a single CERT or vendor can be attacked, "
    "censored, or go offline. Commercial threat feeds are too expensive for "
    "smaller organizations. And informal mailing lists have no way to prove who "
    "actually sent what.")
body(
    "What is needed is a shared system that has the following properties:")
bullet("No single owner — it should run on the computers of all participants.")
bullet("Proof of identity — it should use cryptography to prove who sent each report.")
bullet("Tamper evidence — any change to past data should be visible to everyone immediately.")
bullet("High availability — it should still work even if some nodes go offline.")

h2("2.2 Research Questions")
body("This project tries to answer the following five questions:")
numbered(
    "Can a peer-to-peer blockchain work as a practical platform for sharing "
    "threat data between multiple organizations with proof of origin and tamper "
    "detection?")
numbered(
    "Which consensus method is most appropriate for a network of verified "
    "organizations — Proof-of-Work, Proof-of-Authority, or another approach?")
numbered(
    "How can the system combine guidance from the threat submitter with standard "
    "playbooks, so that every report includes both?")
numbered(
    "How can references to detection tools and trained models be attached to "
    "each threat report, so defenders get not only indicators but also tools to "
    "use against them?")
numbered(
    "What are the performance and storage requirements of a small national "
    "network with between 5 and 50 organizations?")

h2("2.3 Hypothesis")
body(
    "A custom permissioned blockchain with RSA digital signatures on each "
    "submission, Proof-of-Work consensus for the prototype, and a simple "
    "peer-gossip network should be able to provide the integrity, availability, "
    "and attribution that inter-organization threat sharing needs. The system "
    "should be simple enough that a small SOC team or a national CERT can "
    "operate it without needing specialized blockchain engineers.")

h2("2.4 Why This Is Relevant")
body(
    "For Jordan, the impact of this project could be very direct. The Jordan "
    "National CERT, major banks, telecom operators, and larger healthcare "
    "organizations form a natural group of trusted participants. A shared national "
    "instance of ThreatChain would reduce the time between when one Jordanian "
    "organization detects an attack and when the others receive a warning.")
body(
    "For the research community, the project fills a gap that is well-known. As "
    "discussed in Section 4, most academic papers on blockchain-based threat "
    "intelligence sharing stop at design diagrams or partial implementations. A "
    "complete, working, open-source reference implementation gives the field a "
    "concrete starting point.")

page_break()


# ═══════════════════════════════════════════════════════════════
# 3. OBJECTIVES
# ═══════════════════════════════════════════════════════════════

h1("3. Objectives")

h2("3.1 Main Objective")
body(
    "The main objective of this project is to build a working peer-to-peer "
    "blockchain platform that allows verified organizations to share threat "
    "intelligence with digital signatures and tamper detection. The platform "
    "should run on normal computers without needing any specialized hardware, "
    "and it should be possible to demonstrate it on a small network of "
    "independent nodes.")

h2("3.2 Specific Objectives")
for item in [
    "Build a custom Python blockchain using SHA-256 hashing and Proof-of-Work "
    "consensus.",
    "Give each organization a 2048-bit RSA keypair and use RSA-PSS-SHA256 to "
    "sign every submission.",
    "Build a peer-to-peer protocol that allows nodes to register with each other, "
    "exchange chains, and resolve conflicts using the longest-valid-chain rule.",
    "Build a web dashboard that supports organization registration, threat "
    "submission, a live feed, a blockchain explorer, peer management, and "
    "full-text search.",
    "Create a catalog of standard mitigation steps for each threat type, based "
    "on NIST, MITRE ATT&CK, and CISA guidance.",
    "Create a catalog of open-source detection tools and trained-model repositories "
    "on GitHub for each threat type.",
    "Generate a per-threat PDF report with cryptographic attribution that can be "
    "independently verified against the chain.",
    "Test the prototype with a three-node demo network and run a tamper-and-recovery "
    "experiment.",
]:
    numbered(item)

h2("3.3 Success Criteria")
for item in [
    "The system runs end-to-end on normal Windows or Linux hardware without "
    "needing any special setup.",
    "Three nodes can connect to each other and synchronize signed threat "
    "submissions in both directions.",
    "When a node's chain file is deliberately corrupted, the system detects it, "
    "and a consensus sync replaces the bad chain with a valid one from a peer.",
    "Every threat stored on the chain includes a standard mitigation playbook and "
    "a list of detection resources, even if the submitter left those fields empty.",
    "Each threat can be exported as a PDF that includes the cryptographic "
    "signature and block hash for independent verification.",
]:
    bullet(item)

page_break()


# ═══════════════════════════════════════════════════════════════
# 4. RELATED WORK
# ═══════════════════════════════════════════════════════════════

h1("4. Related Work")

body(
    "Several studies in recent years have looked at using blockchain for "
    "cybersecurity and threat data sharing. This section reviews the eight most "
    "relevant papers, describes what each one contributes, and then explains "
    "what gap is still left — which is what this project is trying to address.")

h2("4.1 Blockchain-Based Threat Intelligence Sharing")

body(
    "Wagner et al. (2018) [7] proposed one of the first blockchain-based systems "
    "for sharing cyber threat intelligence. Their system uses a decentralized "
    "approach to share indicators of compromise like malicious IP addresses, "
    "domains, and file hashes. The work was a good step forward because it "
    "improved trust and data integrity compared to centralized feeds. But the "
    "system did not have a practical dashboard, real-time monitoring, or any "
    "guidance on how to respond to the threats it shared.")

body(
    "TrustShare (2024) [1] is the most recent work that is directly related to "
    "this project. It introduces a blockchain framework for secure and "
    "privacy-preserving threat intelligence sharing between organizations. The "
    "system uses Hyperledger Fabric, smart contracts, encryption, and IPFS for "
    "decentralized storage and reports good performance and scalability. "
    "ThreatChain is different because it uses a custom Python blockchain instead "
    "of Hyperledger Fabric, and it focuses on building a complete and deployable "
    "implementation that a small SOC or national CERT can actually use without "
    "needing specialized staff.")

body(
    "DEALER (2023) [5] proposes a decentralized platform for threat intelligence "
    "sharing that uses blockchain and IPFS. Its main contribution is an incentive "
    "system that motivates organizations to participate and share good-quality "
    "reports. The authors show it is practical and efficient. ThreatChain does "
    "not currently include a reputation or incentive mechanism. This is mentioned "
    "in Section 7 as a planned future extension.")

h2("4.2 Foundational Work on Blockchain and Provenance")

body(
    "ProvChain (2017) [3] is an earlier study that uses blockchain to track data "
    "provenance in cloud environments. Its main contribution is demonstrating how "
    "blockchain can create immutable, verifiable records that every participant "
    "can audit independently. ProvChain was not designed for threat intelligence, "
    "but the core blockchain properties it relies on — immutability and "
    "verifiability — are the same properties that make ThreatChain trustworthy.")

body(
    "Nakamoto's 2008 Bitcoin white paper [8] introduced the first practical "
    "permissionless blockchain and the Proof-of-Work consensus algorithm that "
    "this project uses in its prototype. Ethereum's yellow paper by Wood (2014) "
    "[9] expanded the idea to include smart contracts. Castro and Liskov's 1999 "
    "paper on Practical Byzantine Fault Tolerance [10] provides the theoretical "
    "consensus foundation that more efficient permissioned chains are built on, "
    "and it is the basis for the Proof-of-Authority direction described in "
    "Section 7.")

h2("4.3 Standards and Taxonomies")

body(
    "Mavroeidis and Bromander (2017) [4] evaluated existing threat intelligence "
    "taxonomies and the STIX and TAXII sharing standards. Their work shows that "
    "standardized data formats are very important for interoperability between "
    "organizations and security tools. They did not propose a blockchain-based "
    "solution, and they did not address tamper-evidence. ThreatChain can be "
    "extended in the future to support STIX 2.1 and TAXII 2.1, which would "
    "build on what this paper describes.")

body(
    "A systematic literature review updated through 2024 [8] looks at blockchain "
    "applications in cybersecurity across many areas including IoT security, "
    "cryptography, secure storage, and web applications. This review confirms "
    "that blockchain is widely considered a good platform for trust-sensitive "
    "sharing, but also identifies some important challenges: scalability, "
    "privacy, regulatory compliance, and the gap between academic designs and "
    "actual running implementations.")

h2("4.4 IoT and Related Work")

body(
    "Two recent papers explore blockchain in IoT security, which is a related "
    "but different area. Building Trust: IoT Security and Blockchain Integration "
    "(2024) [6] shows how blockchain can improve authentication and data "
    "integrity in IoT environments. BlocFogSec (2024) [2] proposes a blockchain "
    "framework for secure data sharing in IoT fog computing, using smart contracts "
    "and consensus to manage key management and access control. Their results "
    "show better latency, throughput, and attack detection than existing IoT "
    "systems. These papers are relevant as future directions — extending "
    "ThreatChain to handle IoT sensor data would naturally build on this work.")

h2("4.5 The Gap in the Literature")

body(
    "Looking at all eight papers together, three clear patterns appear. First, "
    "many of these systems are conceptual or only partially implemented — very "
    "few provide a complete, working, deployable system. Second, most papers "
    "focus on one or two specific properties like privacy or scalability, rather "
    "than combining all the requirements that a real SOC team would need. Third, "
    "almost none of them include a user-friendly dashboard, search functionality, "
    "real-time feeds, or structured workflows.")

body(
    "There are also other gaps worth mentioning. Many existing systems do not "
    "validate submitted indicators, do not assign confidence scores, and do not "
    "track the reputation of the organizations contributing reports. This means "
    "that low-quality or false reports could be accepted and spread across the "
    "network. Most studies also do not provide actionable guidance — they share "
    "indicators of compromise but not the recommended detection rules, mitigation "
    "steps, or response procedures that analysts need in order to actually act.")

body(
    "Finally, most existing work ignores the regulatory and compliance dimension. "
    "Organizations in banking, healthcare, and government need to keep "
    "tamper-proof records of reported incidents and show compliance with "
    "cybersecurity regulations. Very few existing systems help with this.")

body(
    "ThreatChain tries to address these gaps by combining a working blockchain "
    "core, peer-to-peer networking, a usable dashboard, severity classification, "
    "digital signatures, curated mitigation playbooks, detection-model references, "
    "and exportable PDF reports — all in one deployable system that can run on "
    "the computers of three to fifty organizations without any special "
    "infrastructure.")

page_break()


# ═══════════════════════════════════════════════════════════════
# 5. METHODOLOGY
# ═══════════════════════════════════════════════════════════════

h1("5. Methodology")

h2("5.1 System Overview")
body(
    "Each ThreatChain node has three layers inside it. The top layer is a Flask "
    "web application that shows the dashboard to users and exposes JSON API "
    "endpoints to other nodes. The middle layer is the blockchain core, which "
    "keeps the chain in memory and applies the rules for adding new blocks. The "
    "bottom layer is simple JSON storage on disk — the chain file, the "
    "organization registry, and the peer list.")
body(
    "Every node is independent. Nodes do not need each other for regular "
    "operation. They only contact peers when they want to broadcast a new "
    "threat submission or when they need to resolve a disagreement about which "
    "version of the chain is correct.")
body(
    "As a simple picture to imagine: there are N nodes arranged in a circle. "
    "Each node represents a different organization, for example Jordan CERT, a "
    "bank, or a hospital. Lines between nodes show peer connections. Inside each "
    "node there are three stacked layers: the web app on top, the blockchain "
    "core in the middle, and JSON storage at the bottom.")

h2("5.2 The Blockchain Core")
body(
    "Each block in the chain contains six fields: an index (starting at 0 for "
    "the genesis block), a timestamp, the list of threat transactions inside "
    "that block, the hash of the previous block, a nonce, and the block's own "
    "hash.")
body(
    "The block hash is calculated by converting the block header — everything "
    "except the hash field — into a compact, sorted JSON string, and then "
    "passing it through the SHA-256 algorithm. The result is a 64-character hex "
    "string that uniquely identifies the block.")
body(
    "Mining works as follows: the system picks a nonce value, computes the "
    "hash, and checks if the hash starts with four zeros. If it does, the block "
    "is valid and mining is done. If not, the nonce is increased by one and the "
    "process repeats. At difficulty four, this usually finishes in less than one "
    "second on normal hardware. The difficulty is kept low intentionally so the "
    "demo is fast enough to show during the project defense.")
body(
    "The first block — called the genesis block — is created the same way on "
    "every node: index 0, empty transaction list, and a previous-hash of 64 zero "
    "characters. Because every node builds the genesis block the same way, they "
    "all start with an identical chain root.")
body(
    "The chain is considered valid only if four conditions hold for every block: "
    "the hash matches the block content exactly; the hash satisfies the "
    "difficulty condition; the previous-hash field correctly points to the block "
    "before; and every transaction in the block has a valid digital signature. "
    "If any of these checks fail for any block, the entire chain is considered "
    "invalid.")

h2("5.3 Cryptographic Identity")
body(
    "Each organization is given a 2048-bit RSA keypair when it registers. The "
    "keypair is generated using the Python cryptography library. The public key "
    "is stored in the local registry and shared with peer nodes — it serves as "
    "the organization's identity on the chain. The private key stays on the "
    "organization's own node and is used to sign every threat submission.")
body(
    "The signing algorithm is RSA-PSS with SHA-256 as the hash function and "
    "maximum salt length. RSA-PSS produces a different signature each time it "
    "is called, even for the same data, which is a security advantage. Its "
    "security has been formally proven, and it is recommended in NIST FIPS 186-5 "
    "for new designs instead of the older PKCS#1 v1.5.")
body(
    "Before signing, the transaction data is converted into canonical JSON — "
    "that means keys are sorted alphabetically, there is no extra whitespace, "
    "and it is encoded as UTF-8. This ensures the same bytes are produced every "
    "time the data is serialized, which is important because the signature "
    "verification must produce exactly the same bytes to pass.")

h2("5.4 Peer-to-Peer Protocol")
body(
    "The peer-to-peer protocol is built on HTTP and is designed to be as simple "
    "as possible. It does three main things: peer registration, chain exchange, "
    "and transaction gossip.")
body(
    "For peer registration, a node sends a POST request to another node's "
    "/api/peers/register endpoint, providing its own URL. After this one "
    "exchange, both nodes know about each other.")
body(
    "For chain exchange, a node calls GET /api/chain on each known peer. If "
    "the response contains a chain that is longer than the local one and passes "
    "full validation, the local chain is replaced. This is the longest-valid-"
    "chain rule, which is the same rule used in Bitcoin.")
body(
    "For transaction gossip, when a node finishes mining a new block, it "
    "immediately sends the new transaction to each peer's /api/threats/receive "
    "endpoint. The peer verifies the signature, mines its own copy of the next "
    "block, and saves the updated chain. The chains across peers may temporarily "
    "differ by one block, but the next consensus sync brings them back in "
    "agreement.")

h2("5.5 The Threat Transaction Format")
body(
    "Each threat transaction is a JSON object that contains the following fields:")
bullet("id — a UUID that uniquely identifies this transaction.")
bullet("submitter_pub and submitter_name — the public key and the name of the organization that submitted the report.")
bullet("threat_type and threat_type_custom — one of seven predefined categories, plus an optional custom name when 'other' is selected.")
bullet("severity — one of: critical, high, medium, or low.")
bullet("title and description — a short title and a longer description of the threat.")
bullet("iocs — a list of indicators of compromise such as IP addresses, domains, file hashes, or URLs.")
bullet("mitigation — free-text guidance from the submitter on how to respond.")
bullet("github_links — URLs pointing to detection rules or trained models related to this threat.")
bullet("timestamp — the submission time in Unix epoch seconds.")
bullet("signature — a base64-encoded RSA-PSS signature covering all fields except the signature field itself.")
body(
    "When a node receives a transaction, it verifies it by rebuilding the "
    "canonical JSON bytes from all fields except the signature, and then "
    "checking those bytes against the embedded public key. Embedding the public "
    "key directly in the transaction means any node can verify the signature "
    "independently, even before it has learned about that organization through "
    "peer gossip.")

h2("5.6 The Mitigation Playbook")
body(
    "There is an off-chain Python file called mitigations.py that contains one "
    "playbook for each threat type. Each playbook has a name, a one-line "
    "summary, eight defensive steps, and three authoritative references. The "
    "defensive steps are taken from NIST publications, MITRE ATT&CK, CISA, "
    "SANS, and CIS Controls.")
body(
    "The playbook is stored off-chain deliberately. Defensive practices and "
    "recommended actions change more frequently than historical chain entries "
    "should be modified. By keeping the playbook in source code, it can be "
    "updated quickly without touching the chain's history. The playbook is "
    "displayed in three places in the system: on the submission form itself, "
    "in the expandable details for each threat in the dashboard, and as a "
    "dedicated section in every per-threat PDF report.")

h2("5.7 The Detection-Model Catalog")
body(
    "Alongside each mitigation playbook, the same file lists three or four well-"
    "known open-source GitHub repositories that provide detection rules or "
    "trained models for each threat type. The choices include Yara-Rules/rules "
    "and SigmaHQ/sigma for malware, mitchellkrogza/Phishing.Database for "
    "phishing, Neo23x0/signature-base and Cyb3rWard0g/ThreatHunter-Playbook for "
    "ransomware, montysecurity/C2-Tracker and stamparm/maltrail for command-"
    "and-control, aquasecurity/trivy for vulnerabilities, and firehol/"
    "blocklist-ipsets for DDoS. A generic 'other' category includes MISP, HELK, "
    "and SigmaHQ.")
body(
    "These resources are shown on the submission form, in the threat disclosure "
    "in the dashboard, and in a section of each PDF report. Even if the "
    "submitter did not provide any links of their own, this section is still "
    "useful because it always contains the standard resources for that threat "
    "type.")

h2("5.8 PDF Report Generation")
body(
    "The system provides a URL endpoint — /threats/<id>/report.pdf — that "
    "generates a per-threat PDF on demand using the ReportLab library. The PDF "
    "is divided into six numbered sections: description, indicators of compromise, "
    "the submitter's own mitigation guidance, the standard mitigation playbook, "
    "detection and trained-model resources, and cryptographic provenance. The "
    "provenance section includes the threat ID, the submitter's name, the block "
    "index and hash, the timestamp, and the first 48 characters of the signature. "
    "With this information, any third party can independently verify the PDF "
    "against the chain using the submitter's public key.")

h2("5.9 Implementation Stack")
body(
    "ThreatChain is written in Python 3.12. The web framework is Flask. "
    "Cryptographic operations use the Python cryptography library, which is built "
    "on top of OpenSSL. HTTP requests between peers use the requests library. "
    "PDF generation uses ReportLab. There is no database server — the chain, "
    "the organization registry, and the peer list are all stored as JSON files "
    "inside a per-node folder.")
body(
    "The Python source code is about 600 lines across seven modules: app.py, "
    "blockchain.py, crypto_utils.py, p2p.py, storage.py, mitigations.py, and "
    "pdf_report.py. The frontend uses around ten Jinja2 HTML templates plus one "
    "CSS file of roughly 600 lines. The interactive part of the submission form "
    "uses a small block of plain JavaScript, with no JavaScript framework.")

h2("5.10 Testing and Experiments")
body(
    "The prototype was tested with a three-node network running on a single "
    "laptop, using ports 5000, 5001, and 5002. Each node represented a different "
    "organization. The tests covered organization registration with keypair "
    "generation, threat submission across all seven supported categories, "
    "broadcast and re-verification on all peer nodes, full-text search, and "
    "per-threat PDF generation for each threat type.")
body(
    "The most important test was the tamper-recovery experiment. One byte in a "
    "node's local chain.json file was deliberately changed. On the next page "
    "reload, the blockchain explorer showed the chain as invalid, exactly as "
    "expected. When a consensus sync was triggered, the node fetched the longer "
    "valid chain from a peer and replaced the corrupted local copy. This "
    "experiment directly demonstrates the integrity and automatic recovery "
    "properties that were claimed in the project hypothesis.")

page_break()


# ═══════════════════════════════════════════════════════════════
# 6. SUMMARY
# ═══════════════════════════════════════════════════════════════

h1("6. Summary")

body(
    "This project built and tested ThreatChain, which is a peer-to-peer "
    "blockchain platform for sharing cyber threat intelligence between "
    "organizations. The system uses a custom Python blockchain with SHA-256 "
    "hashing and Proof-of-Work consensus, 2048-bit RSA digital signatures on "
    "every threat submission, a peer-gossip protocol with the longest-valid-"
    "chain rule, and a Flask web dashboard. A curated catalog provides standard "
    "mitigation playbooks and detection-model references for each threat type, "
    "based on NIST, MITRE, and CISA guidance.")
body(
    "The prototype was tested using a three-node network and an explicit tamper-"
    "recovery experiment. The experiment confirmed that the chain correctly "
    "detects byte-level tampering and automatically restores the valid version "
    "from a peer node. Functional testing confirmed that organization "
    "registration, threat submission across seven categories, peer broadcast, "
    "signature verification, and per-threat PDF generation all work end-to-end.")
body(
    "The main contribution of this project is a complete, working, and open-"
    "source reference implementation that fills the gap between theoretical "
    "proposals in the academic literature and expensive centralized commercial "
    "products. The system can be deployed by a small organization or a national "
    "CERT and can be extended for production use.")
body(
    "ThreatChain shows that decentralized, signed, and tamper-evident threat "
    "intelligence sharing is technically achievable using normal hardware and a "
    "relatively small code base. It also shows that the trust and availability "
    "problems of centralized threat feeds can be solved without needing "
    "specialized blockchain platforms or expensive infrastructure.")

page_break()


# ═══════════════════════════════════════════════════════════════
# 7. FUTURE WORK
# ═══════════════════════════════════════════════════════════════

h1("7. Future Work")

body(
    "The following extensions are considered for future development. Each one "
    "is a separate engineering task that builds on the current prototype.")

h2("7.1 Replacing Proof-of-Work with Proof-of-Authority")
body(
    "For a real deployment among a known set of verified validators such as "
    "Jordan CERT and major sector regulators, Proof-of-Work should be replaced "
    "with Proof-of-Authority. This removes the need for mining and gives "
    "deterministic block times. The rest of the system architecture can stay "
    "the same.")

h2("7.2 Adding Traffic Light Protocol (TLP) Privacy Tiers")
body(
    "Some threat data is too sensitive to share openly. For TLP Amber and TLP "
    "Red entries, the actual payload should be stored off-chain in encrypted "
    "form. The on-chain entry would hold only the metadata, the hash of the "
    "encrypted payload, and a key wrapped for each authorized recipient. This "
    "would keep the audit trail while protecting the sensitive content.")

h2("7.3 Adding an Organization Verification Gateway")
body(
    "An out-of-band verification step, managed by the CERT or sector regulator, "
    "should be used to issue signing certificates only to organizations whose "
    "identity has been confirmed. This would prevent Sybil-style fake "
    "registrations.")

h2("7.4 Adding Reputation Scoring")
body(
    "Each organization could build up a reputation score based on how many of "
    "its threat reports are confirmed by others and how many are flagged as "
    "false positives. This is similar to the incentive model proposed in the "
    "DEALER paper [5].")

h2("7.5 Adding STIX 2.1 and TAXII 2.1 Interoperability")
body(
    "Adding native STIX 2.1 import and export plus a TAXII 2.1 transport bridge "
    "would allow ThreatChain to exchange data with existing platforms like MISP "
    "and OpenCTI without needing manual conversion.")

h2("7.6 WebSocket Updates and Mobile Access")
body(
    "The dashboard currently refreshes every six seconds using polling. Switching "
    "to WebSocket push would reduce latency. A read-only mobile companion app "
    "would give analysts and security managers real-time updates from anywhere.")

h2("7.7 Moving the Playbook to a Signed External Feed")
body(
    "At the moment the mitigation playbook and detection catalog are hard-coded "
    "in Python. For a production deployment, they should be hosted as a versioned "
    "and signed external feed, so updates can be rolled out without needing a "
    "new software release.")

h2("7.8 Extending to IoT Telemetry")
body(
    "Building on the IoT security work of BlocFogSec [2] and Building Trust IoT "
    "[6], ThreatChain could be extended to accept signed telemetry from IoT "
    "sensors. This would allow threat detection to be coordinated across IoT "
    "device fleets as well.")

page_break()


# ═══════════════════════════════════════════════════════════════
# REFERENCES
# ═══════════════════════════════════════════════════════════════

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
