"""Build the 2-page ThreatChain proposal PDF in plain English style."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
)
from reportlab.lib.colors import HexColor

OUTPUT = r"C:\Users\abdul\OneDrive\Desktop\idea 2 blockchain\ThreatChain_Proposal_v2.pdf"

NAVY = HexColor("#0d1f3c")
ACCENT = HexColor("#1a4480")


def make_styles():
    base = getSampleStyleSheet()
    return {
        "Title": ParagraphStyle("ThTitle", parent=base["Title"],
            fontName="Helvetica-Bold", fontSize=18, leading=22,
            alignment=TA_CENTER, textColor=NAVY, spaceAfter=4),
        "Subtitle": ParagraphStyle("ThSubtitle", parent=base["Normal"],
            fontName="Helvetica-Oblique", fontSize=11, leading=14,
            alignment=TA_CENTER, textColor=ACCENT, spaceAfter=10),
        "Meta": ParagraphStyle("ThMeta", parent=base["Normal"],
            fontName="Helvetica", fontSize=10, leading=13,
            alignment=TA_CENTER, textColor=HexColor("#444444"), spaceAfter=14),
        "H2": ParagraphStyle("ThH2", parent=base["Heading2"],
            fontName="Helvetica-Bold", fontSize=11.5, leading=14,
            textColor=NAVY, spaceBefore=10, spaceAfter=4, keepWithNext=True),
        "Body": ParagraphStyle("ThBody", parent=base["BodyText"],
            fontName="Times-Roman", fontSize=10, leading=13,
            alignment=TA_JUSTIFY, spaceAfter=4),
        "Bullet": ParagraphStyle("ThBullet", parent=base["BodyText"],
            fontName="Times-Roman", fontSize=10, leading=13,
            alignment=TA_LEFT, leftIndent=14, bulletIndent=4, spaceAfter=2),
    }


def bullets(items, style):
    return [Paragraph(t, style, bulletText="•") for t in items]


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(HexColor("#888888"))
    canvas.drawCentredString(A4[0] / 2, 1.2 * cm, f"Page {doc.page} of 2")
    canvas.drawString(2 * cm, 1.2 * cm, "ThreatChain — Proposal")
    canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, "May 2026")
    canvas.restoreState()


def build_story(s):
    story = []

    story.append(Paragraph(
        "ThreatChain &mdash; Decentralized Threat Intelligence Sharing on Blockchain",
        s["Title"]))
    story.append(Paragraph("Graduation Project Proposal", s["Subtitle"]))
    story.append(Paragraph(
        "<b>Student:</b> [Student Name] &nbsp;&nbsp;|&nbsp;&nbsp; "
        "<b>Supervisor:</b> [Supervisor] &nbsp;&nbsp;|&nbsp;&nbsp; "
        "<b>Date:</b> May 2026", s["Meta"]))

    # 1. Problem
    story.append(Paragraph("1. The Problem", s["H2"]))
    story.append(Paragraph(
        "Cybersecurity organizations &mdash; banks, national CERTs, internet "
        "providers, hospitals &mdash; usually keep what they learn about cyber "
        "attacks to themselves. When one bank discovers a new phishing campaign "
        "on Monday, three more banks may be hit by the same attack by Friday "
        "with no warning. The reason is simple: there is no easy, trusted way "
        "to share threat data with many partners at the same time. "
        "Current options either limit sharing to two parties at a time "
        "(signed email, STIX/TAXII feeds), or depend on a central server "
        "(commercial feeds, single CERT databases) that becomes a target itself.",
        s["Body"]))

    # 2. Solution
    story.append(Paragraph("2. The Proposed Solution &mdash; ThreatChain", s["H2"]))
    story.append(Paragraph(
        "ThreatChain is a peer-to-peer blockchain platform for sharing threat "
        "intelligence between organizations. Every participating organization "
        "runs a node and holds a full copy of the chain. Every threat report "
        "is signed by the sender, sealed into a new block, and shared with all "
        "other nodes. If anyone tries to change a past entry, every node sees "
        "the chain break and rejects the change. The result is a shared, "
        "signed, unchangeable record that no single company controls.",
        s["Body"]))

    # 3. Why blockchain
    story.append(Paragraph("3. Why Blockchain Fits This Problem", s["H2"]))
    story.extend(bullets([
        "<b>No central owner</b> &mdash; removes the single point of failure "
        "and the trust problem of centralized feeds.",
        "<b>Cryptographic signatures</b> &mdash; every report is provably "
        "linked to its sender and cannot be forged.",
        "<b>Linked blocks</b> &mdash; changing any past record breaks the "
        "chain in a way every node can see.",
        "<b>Time proof</b> &mdash; the chain records exactly when each threat "
        "was first reported, useful for compliance and audits.",
    ], s["Bullet"]))

    # PAGE BREAK
    story.append(PageBreak())

    # 4. Architecture
    story.append(Paragraph("4. System Design", s["H2"]))
    story.extend(bullets([
        "<b>Blockchain Core</b> &mdash; a custom Python implementation with "
        "SHA-256 hash chaining and Proof-of-Work consensus.",
        "<b>Identity</b> &mdash; each organization owns a 2048-bit RSA keypair. "
        "The public key is its on-chain identity; the private key signs every "
        "submission using RSA-PSS-SHA256.",
        "<b>Peer-to-Peer</b> &mdash; nodes find each other through peer "
        "registration, exchange chains over HTTP, and use the longest-valid-chain "
        "rule to resolve any disagreement.",
        "<b>Storage</b> &mdash; each node saves its chain, its organization list, "
        "and its peer list as JSON files. No database server needed.",
        "<b>Web Dashboard</b> &mdash; Flask, HTML, CSS, and a small amount of "
        "JavaScript provide registration, threat submission, a live feed, a "
        "blockchain explorer, and peer management.",
    ], s["Bullet"]))

    # 5. Current state
    story.append(Paragraph("5. Where the Project Stands", s["H2"]))
    story.append(Paragraph(
        "A working prototype is complete. Three independent nodes can run on "
        "the same computer or on different computers across a local network. "
        "The full flow has been tested: an organization registers and receives "
        "its keypair; it submits a threat; the threat is signed and mined into "
        "a new block in less than one second; the new block is sent to all "
        "peer nodes, where the signature is verified locally and the block is "
        "added to their chain. A tamper test has also been demonstrated: when "
        "a chain file is deliberately damaged, the system detects the problem "
        "and a consensus sync replaces the bad copy with a good one from a peer.",
        s["Body"]))

    # 6. Deliverables
    story.append(Paragraph("6. What Will Be Delivered", s["H2"]))
    story.extend(bullets([
        "A working multi-node prototype (Python + Flask + HTML/CSS/JavaScript).",
        "An academic report covering motivation, design, implementation, "
        "and evaluation.",
        "A live demonstration including the tamper-and-recovery test.",
        "A written discussion of limitations and future work.",
    ], s["Bullet"]))

    # 7. Limitations
    story.append(Paragraph("7. Known Limitations and Planned Improvements", s["H2"]))
    story.append(Paragraph(
        "The prototype uses Proof-of-Work because it makes the consensus idea "
        "easy to see during the demo. A production deployment would replace it "
        "with Proof-of-Authority, where trusted validators (such as Jordan CERT "
        "and major sector regulators) confirm new blocks without mining. "
        "Privacy of sensitive data will be handled using the Traffic Light "
        "Protocol with off-chain encrypted payloads. Fake-organization risk "
        "(Sybil attacks) will be addressed by an out-of-band verification "
        "gateway that issues signing certificates only after the organization's "
        "identity has been checked. These are documented design extensions, "
        "not unresolved problems.",
        s["Body"]))

    # 8. Discussion
    story.append(Paragraph("8. Discussion Points for the Supervisor", s["H2"]))
    story.extend(bullets([
        "<b>Scope</b> &mdash; is the multi-node software prototype plus the "
        "academic report enough for the graduation requirement, or should a "
        "multi-machine hardware deployment be attempted within the project "
        "timeframe?",
        "<b>Related work</b> &mdash; the student is aware of the existing "
        "literature on blockchain-based threat-intelligence sharing and welcomes "
        "specific recommendations on which papers to cite as primary references.",
        "<b>Optional extensions</b> &mdash; should Proof-of-Authority, TLP tiers, "
        "or the organization-verification gateway be implemented during the "
        "project, or documented only in the Future Work section?",
    ], s["Bullet"]))

    return story


def main():
    s = make_styles()
    doc = SimpleDocTemplate(
        OUTPUT, pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=1.8 * cm, bottomMargin=1.8 * cm,
        title="ThreatChain — Graduation Project Proposal",
        author="ThreatChain",
    )
    doc.build(build_story(s), onFirstPage=footer, onLaterPages=footer)
    print(f"Wrote: {OUTPUT}")


if __name__ == "__main__":
    main()
