"""Build the ThreatChain graduation-project documentation (~20-page Word doc)."""

from docx import Document
from docx.shared import Pt, Inches, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING, WD_BREAK
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUTPUT = r"C:\Users\abdul\OneDrive\Desktop\idea 2 blockchain\ThreatChain_Documentation.docx"

DOC = Document()


# ─────────────────────────── document-wide formatting ───────────────────────────

# Body style
style = DOC.styles["Normal"]
style.font.name = "Times New Roman"
style.font.size = Pt(12)
style.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
style.paragraph_format.line_spacing = 1.15
style.paragraph_format.space_after = Pt(6)

# Heading styles
for h_idx, h_size, h_color in [(1, 18, "1f3864"), (2, 14, "2e75b6"), (3, 12, "2e75b6")]:
    h = DOC.styles[f"Heading {h_idx}"]
    h.font.name = "Calibri"
    h.font.size = Pt(h_size)
    h.font.bold = True
    h.font.color.rgb = RGBColor.from_string(h_color)
    h.paragraph_format.space_before = Pt(18 if h_idx == 1 else 10)
    h.paragraph_format.space_after = Pt(6)
    h.paragraph_format.keep_with_next = True

# Page margins
for section in DOC.sections:
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)

# Footer with centered page number
section = DOC.sections[0]
footer = section.footer
p = footer.paragraphs[0]
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
fld_begin = OxmlElement("w:fldChar"); fld_begin.set(qn("w:fldCharType"), "begin")
instr = OxmlElement("w:instrText"); instr.text = "PAGE"
fld_end = OxmlElement("w:fldChar"); fld_end.set(qn("w:fldCharType"), "end")
r = p.add_run().element
r.append(fld_begin); r.append(instr); r.append(fld_end)


# ─────────────────────────── helpers ───────────────────────────

def add_body(text, *, justify=True, bold=False, italic=False, size=None, indent_first=False):
    p = DOC.add_paragraph()
    if justify:
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if indent_first:
        p.paragraph_format.first_line_indent = Inches(0.3)
    run = p.add_run(text)
    if bold: run.bold = True
    if italic: run.italic = True
    if size: run.font.size = Pt(size)
    return p

def add_h1(text):
    p = DOC.add_heading(text, level=1)
    return p

def add_h2(text):
    p = DOC.add_heading(text, level=2)
    return p

def page_break():
    p = DOC.add_paragraph()
    p.add_run().add_break(WD_BREAK.PAGE)

def add_bullet(text, *, level=0):
    p = DOC.add_paragraph(text, style="List Bullet")
    if level: p.paragraph_format.left_indent = Inches(0.5 * (level + 1))
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    return p

def add_numbered(text):
    p = DOC.add_paragraph(text, style="List Number")
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    return p


# ─────────────────────────── COVER PAGE ───────────────────────────

cover_title = DOC.add_paragraph()
cover_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
for _ in range(6):
    cover_title.add_run().add_break()
r = cover_title.add_run("ThreatChain")
r.font.size = Pt(36); r.font.bold = True
r.font.color.rgb = RGBColor.from_string("1f3864")
r.font.name = "Calibri"

subtitle = DOC.add_paragraph()
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = subtitle.add_run("Decentralized Threat Intelligence Sharing on Blockchain")
r.font.size = Pt(18); r.italic = True
r.font.color.rgb = RGBColor.from_string("2e75b6")
r.font.name = "Calibri"

for _ in range(2):
    DOC.add_paragraph().alignment = WD_ALIGN_PARAGRAPH.CENTER

p = DOC.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Graduation Project Documentation"); r.font.size = Pt(14); r.bold = True

for _ in range(6):
    DOC.add_paragraph()

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


# ─────────────────────────── TABLE OF CONTENTS ───────────────────────────

toc_title = DOC.add_paragraph()
r = toc_title.add_run("Table of Contents"); r.bold = True
r.font.size = Pt(18); r.font.color.rgb = RGBColor.from_string("1f3864")
r.font.name = "Calibri"
DOC.add_paragraph()

# auto-TOC field — Word will populate on first open with right-click → Update Field
p = DOC.add_paragraph()
r = p.add_run()
fld_begin = OxmlElement("w:fldChar"); fld_begin.set(qn("w:fldCharType"), "begin")
instr = OxmlElement("w:instrText"); instr.text = 'TOC \\o "1-2" \\h \\z \\u'
fld_sep = OxmlElement("w:fldChar"); fld_sep.set(qn("w:fldCharType"), "separate")
placeholder = OxmlElement("w:t"); placeholder.text = "Right-click here and choose 'Update Field' to populate the table of contents."
fld_end = OxmlElement("w:fldChar"); fld_end.set(qn("w:fldCharType"), "end")
elem = r.element
elem.append(fld_begin); elem.append(instr); elem.append(fld_sep); elem.append(placeholder); elem.append(fld_end)

page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# 1. INTRODUCTION (3 pages)
# ═══════════════════════════════════════════════════════════════════════════════

add_h1("1. Introduction")

add_h2("1.1 Context and Motivation")
add_body(
    "Cybersecurity has become one of the most consequential disciplines of modern computing. "
    "The frequency and economic impact of cyber-incidents have grown each year, with the 2023 "
    "European Union Agency for Cybersecurity (ENISA) Threat Landscape report documenting an "
    "unprecedented escalation in supply-chain compromises, ransomware against critical "
    "infrastructure, and state-sponsored intrusion campaigns. The WannaCry outbreak of May 2017 "
    "infected more than 200,000 machines across 150 countries within four days, the SolarWinds "
    "supply-chain compromise of December 2020 reached an estimated 18,000 organizations through "
    "a single trusted vendor, and the May 2021 Colonial Pipeline ransomware incident caused fuel "
    "shortages across the eastern United States. Each of these events was preceded by initial "
    "compromise of one organization, followed by rapid lateral exploitation against other "
    "organizations sharing similar attack surfaces.")
add_body(
    "Cyber threat intelligence (CTI) is the structured information that enables defensive teams "
    "to detect attacks earlier, contain them faster, and prevent recurrence. It includes "
    "indicators of compromise (IPs, domains, file hashes, URLs), adversary tactics and "
    "techniques, victim sectors, and recommended defensive responses. The speed at which this "
    "information moves between organizations is decisive: a phishing campaign that targets a "
    "first bank on Monday will typically reach additional banks within the same week. If the "
    "first victim's intelligence reaches the second victim within hours rather than days, the "
    "second's exposure window is reduced by an order of magnitude.")

add_h2("1.2 The Threat Intelligence Sharing Problem")
add_body(
    "Despite the operational value of shared CTI, most organizations possess valuable internal "
    "intelligence that is never shared externally. The reasons are multiple and well documented: "
    "legal-counsel concerns over attribution and liability, competitive considerations, the "
    "absence of trusted bilateral channels with peer organizations, the absence of common "
    "machine-readable formats, and the absence of incentive structures rewarding contribution.")
add_body(
    "The channels that do exist suffer from structural weaknesses. PGP-signed mailing lists "
    "provide authenticity but only between known parties and only in narrative form. The OASIS "
    "STIX and TAXII standards provide a structured format for indicators and a bilateral "
    "transport, but adoption remains uneven and the transport assumes a hub-and-spoke topology. "
    "Commercial threat-intelligence feeds, including products from Anomali, ThreatQuotient, and "
    "Recorded Future, provide curated and machine-readable feeds but at significant cost and "
    "with vendor lock-in. National Computer Emergency Response Team (CERT) databases provide "
    "trusted coordination but introduce a single point of failure and a trust problem: whoever "
    "operates the central server can withhold, alter, or lose alerts, and the central server "
    "itself becomes a high-value target.")
add_body(
    "No widely-deployed mechanism currently provides multi-party sharing of threat intelligence "
    "with cryptographic proof of origin, immutability of the historical record, and absence of a "
    "central owner. This documented gap is the motivation for the present work.")

add_h2("1.3 Why a Blockchain Approach")
add_body(
    "A blockchain ledger exhibits four properties that map directly to the threat-intelligence "
    "sharing problem. First, hash-chained blocks render any tampering with past entries instantly "
    "detectable, because modifying a single byte in block N invalidates the recorded hash of N "
    "and consequently the previous-hash reference of every subsequent block. Second, full "
    "replication of the ledger across every participating node eliminates the single point of "
    "failure inherent in centralized feeds: no individual organization can withhold, alter, or "
    "take the platform down. Third, attaching a digital signature to every entry cryptographically "
    "binds the entry to its originator and prevents forgery by any other participant. Fourth, "
    "the consensus protocol governing block acceptance ensures that new entries are only "
    "appended after the network's validation rules are satisfied, preventing unilateral injection "
    "of invalid or fraudulent intelligence.")
add_body(
    "Together these properties produce a shared, ordered, tamper-evident history — precisely "
    "the property that a multi-organization threat-intelligence ledger requires and that "
    "existing technologies do not deliver simultaneously.")

add_h2("1.4 Project Scope and Contribution")
add_body(
    "ThreatChain is a peer-to-peer blockchain platform for inter-organizational threat-intelligence "
    "sharing. Each participating organization runs an independent node that holds a full copy of "
    "the chain. Every threat submission is cryptographically signed by the originating "
    "organization, sealed into a block via consensus, and gossiped to all peer nodes for "
    "verification and adoption. The prototype is implemented in Python using the Flask web "
    "framework and a custom blockchain core written specifically for this work.")
add_body(
    "ThreatChain is intentionally not a replacement for established security tools. It does not "
    "replace Security Information and Event Management (SIEM) platforms such as Splunk or Elastic, "
    "nor Endpoint Detection and Response (EDR) products such as CrowdStrike Falcon or "
    "SentinelOne, nor open threat-intelligence platforms such as MISP. Rather, it complements "
    "those systems by providing a decentralized, signed record layer that can be ingested by all "
    "of them and that no single party controls.")
add_body(
    "The principal contributions of this work are fourfold: (1) a working full-stack reference "
    "implementation including a custom blockchain, RSA digital signatures, peer-to-peer "
    "networking, and a web-based dashboard; (2) a curated mitigation-playbook system aligned "
    "with the National Institute of Standards and Technology (NIST), the MITRE ATT&CK Framework, "
    "and the Cybersecurity and Infrastructure Security Agency (CISA) guidance; (3) a curated "
    "detection and trained-model catalog referencing 28 well-known open-source security "
    "repositories; (4) per-threat PDF reports that carry cryptographic provenance and can be "
    "shared off-platform while remaining re-verifiable against the chain.")

add_h2("1.5 Document Structure")
add_body(
    "The remainder of this document is organized as follows. Section 2 formalizes the research "
    "statement, including questions and hypothesis. Section 3 enumerates the specific "
    "objectives and success criteria of the work. Section 4 surveys related work across "
    "threat-intelligence platforms, blockchain foundations, and prior academic proposals for "
    "blockchain-based intelligence sharing. Section 5 details the methodology, including system "
    "architecture, the blockchain core, the cryptographic identity scheme, the peer-to-peer "
    "protocol, the data model, the mitigation and detection-model catalogs, the PDF report "
    "generator, the implementation stack, and the validation experiments. Section 6 summarises "
    "the work, and Section 7 identifies concrete extensions for future work. A list of "
    "references closes the document.")

page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# 2. RESEARCH STATEMENT (2 pages)
# ═══════════════════════════════════════════════════════════════════════════════

add_h1("2. Research Statement")

add_h2("2.1 Problem Statement")
add_body(
    "Cyber threat intelligence sharing remains an unsolved coordination problem in operational "
    "cybersecurity. The channels currently in use can be categorized into three groups, each "
    "exhibiting a distinct failure mode. Bilateral channels, exemplified by PGP-signed email "
    "and OASIS STIX feeds exchanged over TAXII transports, provide signed authenticity but do "
    "not scale to N-organization sharing without quadratic configuration cost. Centralized "
    "feeds, whether commercial (Anomali ThreatStream, ThreatQuotient, Recorded Future) or "
    "operated by national CERTs, create both a trust problem and a single point of failure: "
    "the operator can intentionally or accidentally withhold, alter, or lose alerts. Informal "
    "channels, including private mailing lists and chat groups, lack any persistent record, "
    "machine-readability, or signature, and do not survive personnel turnover.")
add_body(
    "What is needed is a distributed, cryptographically-attributed, tamper-evident historical "
    "record of shared threat intelligence that is accessible to all participating organizations "
    "and that no single organization owns or operates. This work investigates whether a "
    "purpose-built permissioned blockchain — with digital signatures per entry and peer-to-peer "
    "consensus — can deliver such a record at the scale and latency required for operational "
    "use among 3-N participating organizations.")

add_h2("2.2 Research Questions")
add_body(
    "The work seeks empirical answers to the following questions:")
add_numbered(
    "Can a peer-to-peer blockchain ledger deliver multi-organization threat-intelligence "
    "sharing with cryptographic proof of origin and tamper-evidence detectable by every "
    "participating node?")
add_numbered(
    "Which consensus mechanism is appropriate for a permissioned threat-intelligence network: "
    "Proof-of-Work (energy-intensive but adversary-agnostic), Proof-of-Authority (efficient but "
    "trust-dependent), or Byzantine Fault Tolerant protocols (efficient but membership-rigid)?")
add_numbered(
    "How can submitter-specific guidance be combined with industry-standard defensive playbooks "
    "per threat type, in a way that preserves the submitter's signed contribution while "
    "automatically attaching authoritative cross-references (NIST, MITRE, CISA)?")
add_numbered(
    "How can references to detection rules and trained classifiers (typically maintained in "
    "external open-source repositories) be attached to indicators of compromise so that downstream "
    "defenders can ingest the detection logic alongside the indicators themselves?")
add_numbered(
    "What are the latency, throughput, and storage implications of a realistic deployment, and "
    "how do they constrain the design choices for production use across 5–50 organizations?")

add_h2("2.3 Hypothesis")
add_body(
    "The work is guided by the following hypothesis: a custom permissioned blockchain "
    "implementing RSA-signed transactions, a lightweight Proof-of-Work consensus protocol "
    "(with a documented transition path to Proof-of-Authority for production deployment), and a "
    "peer-gossip protocol that follows the longest-valid-chain rule can satisfy the integrity, "
    "availability, and attribution requirements of threat-intelligence sharing among three to "
    "several dozen participating organizations, while remaining sufficiently simple to be "
    "implemented and operated by an SME or a national CERT without specialised blockchain "
    "engineering staff.")

add_h2("2.4 Significance")
add_body(
    "The significance of this work is twofold. From a national perspective, the design is "
    "directly applicable to the Jordanian cybersecurity ecosystem: the Jordan National "
    "Computer Emergency Response Team, alongside the major commercial banks, the principal "
    "telecommunications operators, and the larger healthcare networks, collectively form a "
    "natural permissioned consortium that could deploy ThreatChain as a shared national-level "
    "intelligence ledger. Such a deployment would close a documented coordination gap and "
    "reduce the time-to-warning for nationally-targeted campaigns.")
add_body(
    "From an academic perspective, the work contributes a working, demoable, open-source "
    "reference implementation in a space where the literature is dominated by theoretical "
    "proposals and partial prototypes. A complete and runnable artefact — including blockchain "
    "core, cryptographic identity, peer-to-peer networking, web interface, mitigation playbook, "
    "detection catalog, and PDF reporting — gives subsequent researchers and practitioners a "
    "concrete baseline against which to compare new proposals.")

page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# 3. OBJECTIVES (1 page)
# ═══════════════════════════════════════════════════════════════════════════════

add_h1("3. Objectives")

add_h2("3.1 Primary Objective")
add_body(
    "Design, implement, and validate a working peer-to-peer blockchain platform that allows "
    "verified organizations to share signed, tamper-evident threat intelligence with no central "
    "owner, demonstrable on commodity hardware across a small network of independent nodes.")

add_h2("3.2 Secondary Objectives")
for item in [
    "Implement a custom blockchain core in Python featuring SHA-256 hash chaining and "
    "Proof-of-Work consensus.",
    "Implement per-organization cryptographic identity using 2048-bit RSA keypairs with "
    "RSA-PSS-SHA256 signatures over a canonical-JSON serialization of each transaction.",
    "Implement a peer-to-peer protocol providing peer registration, chain gossip, transaction "
    "gossip, and a longest-valid-chain rule for divergence resolution.",
    "Build a web-based dashboard supporting organization registration, threat submission, a "
    "live feed of recent threats, a blockchain explorer, peer management, and full-text search "
    "over threat content.",
    "Build a curated catalog of standard mitigation playbooks per threat type, with each "
    "playbook aligned to authoritative guidance from NIST, MITRE ATT&CK, CISA, SANS, and CIS.",
    "Build a curated catalog of detection rules and trained-model GitHub resources per threat "
    "type, drawing on well-established open-source projects in the security community.",
    "Generate per-threat PDF reports that carry the cryptographic provenance of the chain "
    "entry and can be shared off-platform while remaining independently re-verifiable.",
    "Validate the prototype with a three-node demonstration network and an explicit "
    "tamper-and-recovery experiment.",
]:
    add_numbered(item)

add_h2("3.3 Success Criteria")
for item in [
    "The prototype runs end-to-end on commodity Windows or Linux hardware without "
    "specialised dependencies.",
    "A three-node network successfully synchronizes signed threat submissions in both "
    "directions.",
    "An intentional byte-level tampering of one node's chain is detected, marks the chain "
    "as invalid, and is automatically replaced from peers on consensus sync.",
    "Every threat record on the chain carries an attached standard mitigation playbook and "
    "a list of standard detection resources for its type, even when the submitter provided "
    "neither.",
    "Each threat can be exported as a self-contained PDF that includes the cryptographic "
    "signature and block-hash needed to re-verify the document against the chain.",
]:
    add_bullet(item)

page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# 4. RELATED WORK (5+ pages)
# ═══════════════════════════════════════════════════════════════════════════════

add_h1("4. Related Work")

add_h2("4.1 Threat Intelligence Sharing Platforms")
add_body(
    "The Malware Information Sharing Platform (MISP) is the most widely deployed open-source "
    "threat-intelligence platform. Originally developed by Wagner et al. at the Computer Incident "
    "Response Center Luxembourg, MISP introduces the notion of sharing groups and distribution "
    "levels, allowing organizations to publish indicators with fine-grained visibility — "
    "ranging from a single peer through a named community to public release. MISP supports "
    "export to OASIS STIX 2.x and ingestion via TAXII 2.x, and it provides correlation, tagging, "
    "and a flexible attribute model. However, the architecture remains hub-and-spoke: each MISP "
    "instance is operated by a single organization, and inter-instance synchronization occurs "
    "via bilateral push/pull configurations rather than a shared distributed ledger. No "
    "cryptographic immutability of the historical record is provided beyond what the operating "
    "organization chooses to enforce.")
add_body(
    "OASIS STIX (Structured Threat Information eXpression) and TAXII (Trusted Automated "
    "eXchange of Indicator Information) are the de facto international standards for structured "
    "threat-intelligence content and transport. STIX 2.x is a JSON-based representation of "
    "indicators, threat actors, campaigns, tools, and relationships among them. TAXII 2.x is "
    "the corresponding RESTful transport protocol. The standards are mature and widely "
    "implemented, but the transport is fundamentally bilateral or hub-and-spoke; there is no "
    "TAXII-native notion of a multi-party shared ledger.")
add_body(
    "OpenCTI, developed by the French ANSSI, is a more recent open knowledge-management "
    "platform built on top of the STIX 2.1 data model. It introduces a graph-database view of "
    "threat-intelligence relationships and supports both manual curation and automated ingestion "
    "from external feeds. Like MISP, its inter-instance topology remains organization-centric "
    "rather than ledger-centric.")
add_body(
    "On the commercial side, products such as Anomali ThreatStream, ThreatQuotient, and "
    "Recorded Future provide curated, machine-readable feeds with significant value-added "
    "enrichment (geo-location, actor attribution, machine-learning classifications). Their "
    "weaknesses for the present problem are well documented: significant subscription cost, "
    "vendor lock-in over the analytical pipeline, and a trust requirement that the vendor will "
    "not withhold or alter alerts.")
add_body(
    "National CERT programs and the Carnegie Mellon CERT Coordination Center (CERT-CC) provide "
    "the trusted-coordinator role at the national and international levels. They are essential "
    "but, by definition, centralized; their availability and integrity rest on the operating "
    "agency.")

add_h2("4.2 Blockchain Foundations")
add_body(
    "The blockchain abstraction was popularized by Nakamoto's 2008 Bitcoin whitepaper, which "
    "introduced a permissionless distributed ledger secured by Proof-of-Work consensus. In "
    "Bitcoin, blocks are appended to the chain by miners who expend computational work to find "
    "a nonce that makes the block's SHA-256 hash satisfy a network-wide difficulty target. The "
    "scheme provides probabilistic finality and tamper-evidence: rewriting any past block "
    "requires re-doing the work for that block and every subsequent block while simultaneously "
    "outpacing the honest network.")
add_body(
    "Wood's 2014 Ethereum yellow paper generalised the Bitcoin model by introducing a "
    "Turing-complete virtual machine for smart contracts on the same Proof-of-Work substrate. "
    "Subsequent blockchain platforms diverge primarily in their consensus protocol. Proof-of-Stake "
    "(used by Ethereum since the Merge in 2022) replaces computational work with stake-based "
    "voting. Practical Byzantine Fault Tolerance (Castro and Liskov, 1999) achieves "
    "deterministic finality among known validators tolerant of up to one third Byzantine "
    "members and underlies several permissioned platforms. Proof-of-Authority is an even "
    "simpler variant suitable when the set of validators is small, pre-approved, and reputable.")
add_body(
    "A critical distinction for the present work is permissionless versus permissioned operation. "
    "Permissionless blockchains (Bitcoin, Ethereum, Litecoin) admit any party as a node and "
    "rely on economic incentives to deter Sybil attacks; their consensus protocols are "
    "necessarily expensive. Permissioned blockchains (Hyperledger Fabric, ConsenSys Quorum, "
    "R3 Corda) restrict the validator set to known parties and can therefore adopt much more "
    "efficient consensus protocols. For inter-organizational data sharing among a known and "
    "verified set of organizations — banks, CERTs, telecoms, hospitals — a permissioned model "
    "is the natural fit, and is the model adopted by ThreatChain.")

add_h2("4.3 Prior Academic Work on Blockchain-based Threat Intelligence")
add_body(
    "The intersection of blockchain technology and threat intelligence has produced a body of "
    "academic literature spanning the last several years. Wagner et al.'s 2016 paper describing "
    "the design and implementation of MISP serves as a baseline for non-blockchain sharing and "
    "is widely cited as the canonical reference for inter-organizational CTI exchange.")
add_body(
    "Menges and Pernul (2018) examined the comparative landscape of incident reporting formats "
    "and identified the integrity, auditability, and non-repudiation requirements that map "
    "naturally to blockchain-recorded entries. Their analysis informs the present work's "
    "decision to attach an RSA digital signature to every chain entry rather than relying on "
    "network-level authentication.")
add_body(
    "Riesco, Larriva-Novo, and Villagrá (2020) propose a blockchain-based knowledge-exchange "
    "framework for cyber threat intelligence in Telecommunication Systems. Their design "
    "anticipates the value of a shared distributed record but stops short of a runnable, "
    "demoable reference implementation. Homan, Shiel, and Thorpe (2019) likewise propose a "
    "blockchain-network model for CTI sharing, focusing on the protocol design.")
add_body(
    "Putz, Menges, and Pernul, and several subsequent authors, have explored variations on "
    "this theme — adding privacy-preserving disclosure controls, reputation scoring, and "
    "smart-contract-based reward mechanisms. Across this body of work, two recurring "
    "observations stand out: (a) the consensus around blockchain as a candidate substrate is "
    "strong, but (b) the field is dominated by paper designs and partial prototypes rather than "
    "complete, runnable, full-stack implementations that an organization could deploy without "
    "substantial additional engineering effort.")

add_h2("4.4 Cryptographic Identity, Signing, and Attribution")
add_body(
    "Digital signatures are the primary mechanism by which entries on a permissionless or "
    "permissioned ledger are bound to their originators. The RSA Probabilistic Signature Scheme "
    "(RSA-PSS), standardised in PKCS #1 v2.1 and reaffirmed in NIST FIPS 186-5, is a modern "
    "RSA signature scheme that randomises the padding and is provably secure under the "
    "RSA assumption in the random-oracle model. It is preferred over the older PKCS #1 v1.5 "
    "scheme for new designs. ThreatChain adopts RSA-PSS with SHA-256 and the maximum permitted "
    "salt length.")
add_body(
    "The Pretty Good Privacy (PGP) and OpenPGP standards provide a long-running counter-example "
    "to centralized Public Key Infrastructure (PKI): trust is established through a peer-signed "
    "web rather than through hierarchical certificate authorities. The PGP model has proven "
    "robust over decades for individual identity attestation but does not scale well to "
    "organization-level high-availability operations. ThreatChain takes a position between these "
    "two extremes: each organization holds a self-managed keypair (PGP-like), but the "
    "out-of-band registration step is performed by a single trusted gateway (a CERT-like role) "
    "in production deployments.")
add_body(
    "The World Wide Web Consortium's Decentralized Identifier (DID) specification, finalised "
    "as a W3C Recommendation in 2022, provides a more recent abstraction for identifiers that "
    "are not tied to a central registry. DIDs are a natural future direction for the present "
    "work, supplanting the ad-hoc 'fingerprint' identifier currently used.")

add_h2("4.5 Gaps and Position of This Work")
add_body(
    "Three gaps in the existing literature and industry practice motivate the present work. "
    "First, no open and ready-to-deploy reference implementation exists that combines a "
    "blockchain ledger, RSA-signed transactions, a curated mitigation playbook system, and a "
    "curated detection-resource catalog — these elements have been proposed individually but "
    "not assembled into a runnable artefact. Second, most academic prototypes in the area stop "
    "at protocol design, leaving the substantial engineering effort of building a full-stack "
    "web application, a peer-to-peer transport, and a usable defender experience to subsequent "
    "implementers. Third, commercial systems that approach these requirements are proprietary, "
    "expensive, and create vendor lock-in over both the data and the analytical pipeline.")
add_body(
    "ThreatChain occupies a deliberately practical position in this landscape. It is positioned "
    "as an educational, modifiable reference implementation that an SME, a sector regulator, or "
    "a national CERT — particularly in jurisdictions such as Jordan that lack a national "
    "shared-ledger CTI platform — could fork, configure, and deploy without specialised "
    "blockchain engineering staff. The trade-offs made in favour of demonstrability (Proof-of-Work "
    "instead of Proof-of-Authority, single-language Python implementation rather than polyglot "
    "production stack, JSON storage rather than a database server) are documented and revisited "
    "in the Future Work section.")

page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# 5. METHODOLOGY (6 pages)
# ═══════════════════════════════════════════════════════════════════════════════

add_h1("5. Methodology")

add_h2("5.1 System Architecture Overview")
add_body(
    "The system is structured in three logical layers per node. The outermost layer is the "
    "network of peer nodes, each operated by an independent organization and connected to the "
    "others over HTTP. Each node runs an identical web application implemented in the Flask "
    "framework, which exposes the dashboard pages to end users and the JSON API endpoints to "
    "peer nodes. The application is backed by a custom blockchain core and a per-node JSON "
    "storage layer holding the chain, the organization registry, and the peer list. Every node "
    "holds a complete copy of the chain and does not depend on any other node for its day-to-day "
    "operation; peer connections exist solely for the propagation of new submissions and the "
    "resolution of forks via the longest-valid-chain rule.")
add_body(
    "Figure 5.1 (described textually here) depicts N peer nodes — each labeled with the "
    "organization it represents, such as Jordan CERT, Acme Bank, Memorial Hospital — connected "
    "to one another by directed peer links. Each node contains a stack of three boxes "
    "representing, top to bottom, the Flask web application (with five page routes and seven "
    "JSON API endpoints), the blockchain core (Block, Blockchain, Proof-of-Work, and validation "
    "components), and the JSON storage (chain.json, orgs.json, peers.json).")

add_h2("5.2 Blockchain Core")
add_body(
    "Each block is represented by a Python dataclass with six fields: an index (zero for the "
    "genesis block and incrementing thereafter), a Unix-epoch timestamp, a list of threat "
    "transactions, the hash of the previous block (a 64-hexadecimal-character SHA-256 digest), "
    "a nonce (the integer found by mining), and the block's own hash. The block hash is computed "
    "by serialising the block header (everything except the hash field itself) to canonical "
    "JSON — with sorted keys, compact separators, and no whitespace — and applying the SHA-256 "
    "algorithm to the UTF-8 encoding of the resulting string.")
add_body(
    "The Proof-of-Work mining procedure searches for an integer nonce that, when inserted into "
    "the block header, yields a SHA-256 hash whose hexadecimal representation begins with a "
    "configured number of zeros (the difficulty parameter). The default difficulty in the "
    "prototype is four, which on commodity hardware typically completes in under one second per "
    "block. The choice of four was driven by demonstrability: a higher difficulty would make "
    "the live mining demonstration during the project defence visibly slow. The mining loop "
    "is straightforward; it increments the nonce until the hash satisfies the target, then "
    "writes the discovered hash to the block.")
add_body(
    "The genesis block is constructed deterministically with index zero, timestamp zero, an "
    "empty transactions list, and a previous_hash field consisting of 64 zero characters. It is "
    "mined at node startup and persisted alongside any subsequent blocks. The chain-validation "
    "procedure asserts four invariants for every block: the recomputed hash equals the stored "
    "hash; the hash satisfies the difficulty target; the previous_hash equals the hash of the "
    "preceding block; and every transaction within the block has a valid signature. A single "
    "violated invariant causes the entire chain to be reported invalid.")

add_h2("5.3 Cryptographic Identity")
add_body(
    "Each organization owns a 2048-bit RSA keypair generated at registration time using the "
    "Python cryptography library (which wraps OpenSSL). The public key is the organization's "
    "on-chain identity: it is stored in the local organization registry, gossiped to peer nodes "
    "during chain synchronization, and embedded in every transaction signed by the organization. "
    "The private key remains exclusively on the originating node and is used only to sign new "
    "submissions. Storage of the private key in plaintext within the prototype is a deliberate "
    "demonstrability choice; the Future Work section discusses encryption at rest.")
add_body(
    "Signatures are produced using RSA-PSS with SHA-256 as the hash function and the maximum "
    "permitted PSS salt length. RSA-PSS is a probabilistic signature scheme with stronger "
    "security proofs than the older PKCS #1 v1.5 scheme; it is mandated for new uses by NIST "
    "FIPS 186-5. The message under signature is a canonical JSON serialisation of the "
    "transaction payload (all fields except the signature itself), with sorted keys and compact "
    "separators. This canonical form ensures that any node — regardless of implementation "
    "language — that re-serialises the same payload produces identical bytes and therefore "
    "verifies the signature successfully.")

add_h2("5.4 P2P Protocol")
add_body(
    "The peer-to-peer protocol is intentionally minimal and built on HTTP. A node learns about "
    "a peer either at startup (via a command-line --peer flag) or through the Peers tab in the "
    "dashboard. Adding a peer triggers a POST request to that peer's /api/peers/register "
    "endpoint, supplying the local node's public URL. The peer records the URL in its own peer "
    "list, achieving mutual awareness without any central directory.")
add_body(
    "Chain exchange is initiated explicitly by a node calling the Trigger Consensus Sync action "
    "or implicitly at startup. The initiating node calls GET /api/chain on each peer, retrieves "
    "the peer's chain as JSON, and compares its length with the local chain. If the peer's "
    "chain is strictly longer and passes complete validation (hash, Proof-of-Work, and signature "
    "checks for every block), the local chain is replaced. This is Nakamoto's longest-valid-chain "
    "rule, restricted here to a permissioned context where every chain is expected to be valid "
    "but timing differences during simultaneous submissions may produce temporary forks.")
add_body(
    "Transaction gossip occurs on each new submission. The originating node, after sealing the "
    "transaction into a new block via Proof-of-Work, calls POST /api/threats/receive on every "
    "known peer URL. The peer's handler verifies the transaction's signature, accepts the "
    "transaction into its own pending pool, and mines its own next block. Convergence to a "
    "single chain is then handled either at the next consensus sync or implicitly when the "
    "longest-valid-chain rule resolves the temporary fork.")

add_h2("5.5 Threat Transaction Data Model")
add_body(
    "Each threat transaction is a JSON dictionary with the following fields: a UUID identifier "
    "(id); the submitter's RSA public key in PEM format (submitter_pub); the human-readable "
    "submitter name (submitter_name); the threat type (one of malware, phishing, ransomware, "
    "c2, vulnerability, ddos, or other); an optional submitter-supplied custom type name "
    "(threat_type_custom, used when threat_type is 'other'); a severity (critical, high, "
    "medium, or low); a short title; a longer description; a list of indicators of compromise "
    "(iocs); the submitter-supplied free-text mitigation; a list of submitter-supplied URLs "
    "pointing to detection rules or trained-model repositories (github_links); a "
    "submission timestamp; and the base64-encoded RSA-PSS signature.")
add_body(
    "Verification of a transaction reconstructs the canonical JSON payload omitting the "
    "signature field and invokes the cryptography library to verify the signature against the "
    "submitter's embedded public key. The choice to embed the public key in every transaction "
    "(rather than referencing it indirectly via a fingerprint that resolves to an "
    "organization-registry entry) is a robustness measure: a transaction is independently "
    "verifiable using only the bytes within the transaction itself, even by a fresh node that "
    "has not yet learned about the originating organization through peer gossip.")

add_h2("5.6 Standard Mitigation Playbook System")
add_body(
    "An off-chain Python catalog, contained in the mitigations module, holds one playbook "
    "entry per supported threat type. Each entry comprises a human-readable name, a one-sentence "
    "summary of the threat class, an ordered list of eight defensive steps, and three "
    "authoritative external references. The defensive steps are drawn from established "
    "guidance — NIST Special Publications, MITRE ATT&CK Mitigations, CISA Stop-Ransomware Guide "
    "and KEV Catalog, the SANS Internet Storm Center, and the Center for Internet Security "
    "Critical Security Controls. The references provide the citation chain that an examiner or "
    "downstream defender can follow to validate each step.")
add_body(
    "The catalog is deliberately maintained outside the blockchain rather than within it. "
    "Defensive practices evolve more rapidly than blockchain entries should be rewritten, and "
    "tying the catalog to the immutable record would create operational friction whenever "
    "guidance is updated. The catalog is rendered in three places: live on the threat-submission "
    "form (the panel updates instantly as the user changes the threat-type dropdown), within the "
    "expandable disclosure under each threat row on the dashboard and explorer pages, and as "
    "Section 4 of every per-threat PDF report.")

add_h2("5.7 Standard Detection-Model Catalog")
add_body(
    "A parallel curated field in the same off-chain catalog lists three to four well-known "
    "open-source security GitHub repositories per threat type, each with a short description and "
    "the canonical URL. The selection prioritises repositories with established community "
    "presence and citation in operational SOC literature. For malware: the YARA-Rules community "
    "rule repository, SigmaHQ Sigma rules, the Neo23x0 signature-base used by the Loki scanner, "
    "and Mandiant's capa capability-detection tool. For phishing: mitchellkrogza's "
    "Phishing.Database, the OpenPhish public feed, phishfort-lists, and the JPCERT/CC "
    "phishurl-list. For ransomware: the YARA subfolder of signature-base, the Cyb3rWard0g "
    "ThreatHunter-Playbook, redcanaryco's atomic-red-team, and Elastic's protections-artifacts. "
    "For command-and-control: montysecurity's C2-Tracker, stamparm's maltrail, ESET's "
    "malware-ioc, and the Sigma network-category rules. For vulnerabilities: aquasecurity's "
    "trivy, the CVEProject cvelistV5, OWASP Dependency-Check, and the CISA KEV public mirror. "
    "For DDoS: firehol's blocklist-ipsets, stamparm's ipsum, an open ML DDoS-Attack-Detection "
    "project, and FastNetMon. The generic 'other' category points to MISP, MISP warning-lists, "
    "the HELK platform, and SigmaHQ.")
add_body(
    "Like the playbook catalog, this catalog is rendered on the submission form (with a 'copy "
    "to my links' button that appends the standard URLs to the submitter's textarea), within "
    "the threat-row disclosure, and as Section 5 of each per-threat PDF.")

add_h2("5.8 PDF Report Generation")
add_body(
    "Per-threat PDF reports are generated on demand by the /threats/<id>/report.pdf endpoint, "
    "implemented using the ReportLab library. The endpoint locates the threat by identifier in "
    "any block on the chain, retrieves the corresponding standard playbook from the off-chain "
    "catalog, and renders a six-section document. Section 1 is the textual description. "
    "Section 2 is a bulleted, monospace-formatted list of indicators. Section 3 is the "
    "submitter's specific mitigation, with a fallback notice when none was provided. Section 4 "
    "is the full standard mitigation playbook including authoritative references. Section 5 "
    "combines submitter-provided detection links with the curated standard detection resources. "
    "Section 6 is the cryptographic provenance: threat identifier, submitter name, sealing "
    "block index, block hash, submission timestamp, and a truncated representation of the "
    "RSA-PSS signature. A closing paragraph documents that the PDF can be re-verified against "
    "the chain by any peer node holding the originating organization's public key.")

add_h2("5.9 Implementation Stack")
add_body(
    "The implementation language is Python 3.12. The web framework is Flask. The cryptography "
    "primitives are provided by the cryptography library (which wraps OpenSSL). HTTP between "
    "peer nodes uses the requests library. PDF generation uses ReportLab. There is no database "
    "server in the dependency graph; all persistence is via JSON files held in a per-node data "
    "directory. The total Python source code is approximately 600 lines across seven modules: "
    "app.py (Flask routes), blockchain.py (Block and Blockchain dataclasses, Proof-of-Work, "
    "validation), crypto_utils.py (RSA key generation, signing, verification, canonicalisation), "
    "p2p.py (peer-gossip functions), storage.py (per-node JSON persistence), mitigations.py "
    "(the off-chain playbook and detection-model catalog), and pdf_report.py (the per-threat "
    "PDF builder). The frontend consists of approximately ten Jinja2 templates and a single "
    "stylesheet of roughly 600 lines; a single inline JavaScript block on the submission form "
    "provides the live update of the standard playbook and detection-model panels. No frontend "
    "framework is used.")

add_h2("5.10 Validation and Experimentation")
add_body(
    "The prototype was validated through a three-node demonstration network running on a single "
    "host (localhost ports 5000, 5001, and 5002), each instance representing a different "
    "organization (Jordan CERT, Acme Bank, Memorial Hospital). Functional tests covered: "
    "organization registration with keypair generation, threat submission across all seven "
    "supported types (including the custom 'other' type), peer-to-peer broadcast and "
    "re-verification of signatures on each receiving node, full-text search across the chain, "
    "and per-threat PDF generation in every category.")
add_body(
    "A tamper-recovery experiment was performed by deliberately corrupting a single byte within "
    "one node's chain.json file while the other two nodes remained intact. On reload, the "
    "tampered node's Blockchain Explorer correctly reported the chain as invalid. Triggering a "
    "consensus synchronisation caused the tampered node to fetch the longer valid chain from "
    "either peer, replace its local copy, and return to a valid state. This experiment "
    "directly validates the integrity and recovery properties claimed in Section 2.3.")
add_body(
    "PDF generation was tested for each threat type with both populated and empty "
    "submitter-provided mitigation and detection-link fields; the resulting PDFs uniformly "
    "contained the type-specific standard playbook in Section 4 and the standard detection "
    "resources in Section 5, with the appropriate fallback notice in Section 3 when the "
    "submitter had not supplied incident-specific mitigation.")

page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# 6. SUMMARY (1 page)
# ═══════════════════════════════════════════════════════════════════════════════

add_h1("6. Summary")

add_body(
    "This work designed, implemented, and validated ThreatChain, a peer-to-peer "
    "blockchain platform for inter-organizational threat-intelligence sharing. The platform "
    "consists of a custom Python blockchain core with SHA-256 hash chaining and Proof-of-Work "
    "consensus, per-organization 2048-bit RSA cryptographic identities with RSA-PSS-SHA256 "
    "signed transactions, a peer-to-peer protocol implementing peer registration and the "
    "longest-valid-chain rule, and a Flask-based web dashboard providing registration, "
    "submission, live feed, blockchain exploration, peer management, and search. A curated "
    "off-chain catalog supplies a standard mitigation playbook and a set of well-known "
    "detection and trained-model resources for each supported threat type, both aligned with "
    "NIST, MITRE, CISA, and equivalent authoritative guidance.")
add_body(
    "Validation was performed using a three-node demonstration network and an explicit "
    "tamper-recovery experiment, in which a deliberately corrupted local chain was detected as "
    "invalid and automatically replaced via consensus synchronisation from peers. End-to-end "
    "functional tests covered organization registration, threat submission across seven "
    "categories, peer broadcast, signature re-verification, and per-threat PDF report generation. "
    "Every threat on the chain, regardless of the submitter's effort in filling free-text "
    "fields, carries an attached standard playbook and a curated list of detection resources.")
add_body(
    "The principal contribution of this work is a complete, runnable, open-source reference "
    "implementation that fills a documented gap between theoretical blockchain-CTI proposals and "
    "commercial centralized feeds, suitable for adoption and extension by SMEs and national "
    "CERT programmes.")
add_body(
    "ThreatChain demonstrates that decentralized, signed, tamper-evident threat-intelligence "
    "sharing is technically achievable on commodity hardware with a small, auditable codebase, "
    "and that the long-standing trust and availability problems of centralized CTI feeds can "
    "be addressed without recourse to specialised blockchain platforms or proprietary tooling.")

page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# 7. FUTURE WORK (1 page)
# ═══════════════════════════════════════════════════════════════════════════════

add_h1("7. Future Work")

add_body(
    "Several concrete extensions are identified for future iterations of the system. Each is "
    "scoped to a self-contained engineering effort building on the present prototype.")

add_h2("7.1 Migration to Proof-of-Authority Consensus")
add_body(
    "For a production deployment among verified validators, such as Jordan CERT and the "
    "principal sector regulators, Proof-of-Work should be replaced with Proof-of-Authority. "
    "This change preserves the validation pipeline and chain structure while eliminating the "
    "computational overhead of mining and yielding deterministic block times.")

add_h2("7.2 Traffic Light Protocol Tiers and Off-chain Encrypted Payloads")
add_body(
    "Sensitive intelligence (TLP Amber or Red) should be stored off-chain as an encrypted "
    "payload while the on-chain entry retains only the metadata, the encrypted payload's hash, "
    "and a recipient-specific key wrap. This design preserves the audit trail of the on-chain "
    "record while satisfying the confidentiality requirements of higher TLP tiers.")

add_h2("7.3 Organization Verification Gateway")
add_body(
    "An out-of-band verification gateway, operated by the CERT or sector regulator, should "
    "issue signing certificates to organizations only after identity verification. This "
    "eliminates the Sybil-registration risk inherent in the current open-registration prototype "
    "and aligns the platform with the trust model already used by MISP communities.")

add_h2("7.4 Reputation Scoring")
add_body(
    "Each organization should accumulate a reputation score based on how many of its submitted "
    "threats are independently confirmed by peers and how few are flagged as false positives. "
    "The score should be visible on the threat row and provide a soft trust signal alongside "
    "the cryptographic provenance.")

add_h2("7.5 Native STIX 2.1 / TAXII 2.1 Interoperability")
add_body(
    "Inbound and outbound bridges to the OASIS STIX 2.1 and TAXII 2.1 standards would allow "
    "ThreatChain to consume from and publish to existing MISP and OpenCTI instances without "
    "manual data transformation.")

add_h2("7.6 WebSocket Live Feed and Mobile Client")
add_body(
    "The current dashboard polls every six seconds. A WebSocket-based push channel would "
    "eliminate the polling latency and bandwidth cost. A complementary read-only mobile client "
    "would provide on-call executives and analysts with real-time situational awareness.")

add_h2("7.7 Signed External Catalog")
add_body(
    "The mitigation and detection-model catalogs are currently embedded in Python source. A "
    "production design should migrate them to a versioned, signed external feed, allowing "
    "rapid updates without redeploying the application and preserving an audit trail of "
    "catalog revisions.")

page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# REFERENCES (1 page)
# ═══════════════════════════════════════════════════════════════════════════════

add_h1("References")

REFS = [
    "Nakamoto, S. (2008). Bitcoin: A Peer-to-Peer Electronic Cash System. White paper.",
    "Wood, G. (2014). Ethereum: A Secure Decentralised Generalised Transaction Ledger. Ethereum Yellow Paper, EIP-150 revision.",
    "Castro, M., & Liskov, B. (1999). Practical Byzantine Fault Tolerance. In Proceedings of the Third USENIX Symposium on Operating Systems Design and Implementation (OSDI '99), pp. 173–186.",
    "Wagner, C., Dulaunoy, A., Wagener, G., & Iklody, A. (2016). MISP: The Design and Implementation of a Collaborative Threat Intelligence Sharing Platform. In Proceedings of the 2016 ACM Workshop on Information Sharing and Collaborative Security (WISCS '16), pp. 49–56.",
    "National Institute of Standards and Technology. (2016). NIST Special Publication 800-150: Guide to Cyber Threat Information Sharing. C. Johnson, L. Badger, D. Waltermire, J. Snyder, and C. Skorupka.",
    "National Institute of Standards and Technology. (2012). NIST Special Publication 800-61 Revision 2: Computer Security Incident Handling Guide. P. Cichonski, T. Millar, T. Grance, and K. Scarfone.",
    "National Institute of Standards and Technology. (2013). NIST Special Publication 800-83 Revision 1: Guide to Malware Incident Prevention and Handling for Desktops and Laptops. M. Souppaya and K. Scarfone.",
    "National Institute of Standards and Technology. (2019). NIST Special Publication 800-177 Revision 1: Trustworthy Email. R. Chandramouli, S. Garfinkel, S. Nightingale, and S. Rose.",
    "National Institute of Standards and Technology. (2023). FIPS Publication 186-5: Digital Signature Standard (DSS).",
    "OASIS Cyber Threat Intelligence Technical Committee. (2021). STIX Version 2.1, OASIS Standard.",
    "OASIS Cyber Threat Intelligence Technical Committee. (2021). TAXII Version 2.1, OASIS Standard.",
    "Menges, F., & Pernul, G. (2018). A comparative analysis of incident reporting formats. Computers & Security, 73, 87–101.",
    "Riesco, R., Larriva-Novo, X., & Villagrá, V. A. (2020). Cybersecurity threat intelligence knowledge exchange based on blockchain. Telecommunication Systems, 73, 259–288.",
    "Homan, D., Shiel, I., & Thorpe, C. (2019). A new network model for cyber threat intelligence sharing using blockchain technology. In Proceedings of the 10th IFIP International Conference on New Technologies, Mobility and Security (NTMS), pp. 1–6.",
    "MITRE Corporation. (2024). ATT&CK Enterprise Matrix v15. https://attack.mitre.org/",
    "Cybersecurity and Infrastructure Security Agency. (2023). #StopRansomware Guide. https://www.cisa.gov/stopransomware/ransomware-guide",
    "Cybersecurity and Infrastructure Security Agency. Known Exploited Vulnerabilities Catalog. https://www.cisa.gov/known-exploited-vulnerabilities-catalog",
    "Center for Internet Security. (2021). CIS Critical Security Controls Version 8.",
    "European Union Agency for Cybersecurity. (2023). ENISA Threat Landscape Report.",
    "Sporny, M., Longley, D., Sabadello, M., Reed, D., & Steele, O. (2022). Decentralized Identifiers (DIDs) v1.0. W3C Recommendation, 19 July 2022.",
]
for i, r in enumerate(REFS, 1):
    p = DOC.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.left_indent = Inches(0.4)
    p.paragraph_format.first_line_indent = Inches(-0.4)
    run = p.add_run(f"[{i}]  ")
    run.bold = True
    p.add_run(r)


# ─────────────────────────── save ───────────────────────────

DOC.save(OUTPUT)
print(f"Wrote: {OUTPUT}")
