"""Per-threat PDF report generator.

Given a single threat transaction and the block that sealed it, build a
professional PDF that contains: threat details, IOCs, mitigation, GitHub
links to trained detection models, and the cryptographic proof
(block hash, signature fingerprint).
"""

from __future__ import annotations

import io
import time
from typing import Iterable

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether,
)
from reportlab.lib.colors import HexColor

# palette — kept warm and ink-friendly so the PDF looks professional on paper
NAVY = HexColor("#0d1f3c")
AMBER = HexColor("#b45309")     # darker amber, prints better than #f59e0b
ROSE = HexColor("#be123c")
MUTED = HexColor("#5b6477")
LIGHT = HexColor("#f5f7fb")
DIVIDER = HexColor("#d9dee9")


SEVERITY_COLOR = {
    "critical": HexColor("#b91c1c"),
    "high":     HexColor("#c2410c"),
    "medium":   HexColor("#a16207"),
    "low":      HexColor("#5b21b6"),
}


def _styles():
    base = getSampleStyleSheet()
    return {
        "Title": ParagraphStyle("RTitle", parent=base["Title"],
                                fontName="Helvetica-Bold", fontSize=18, leading=22,
                                textColor=NAVY, spaceAfter=4, alignment=TA_LEFT),
        "Subtitle": ParagraphStyle("RSub", parent=base["Normal"],
                                   fontName="Helvetica", fontSize=10, leading=14,
                                   textColor=MUTED, spaceAfter=14),
        "Eyebrow": ParagraphStyle("REyebrow", parent=base["Normal"],
                                  fontName="Helvetica-Bold", fontSize=8.5, leading=11,
                                  textColor=AMBER, spaceAfter=2),
        "H2": ParagraphStyle("RH2", parent=base["Heading2"],
                             fontName="Helvetica-Bold", fontSize=11.5, leading=14,
                             textColor=NAVY, spaceBefore=12, spaceAfter=5,
                             keepWithNext=True),
        "Body": ParagraphStyle("RBody", parent=base["BodyText"],
                               fontName="Times-Roman", fontSize=10, leading=14,
                               alignment=TA_JUSTIFY, spaceAfter=4, textColor=NAVY),
        "Mono": ParagraphStyle("RMono", parent=base["BodyText"],
                               fontName="Courier", fontSize=9, leading=12,
                               textColor=NAVY, spaceAfter=2),
        "Link": ParagraphStyle("RLink", parent=base["BodyText"],
                               fontName="Courier", fontSize=9, leading=13,
                               textColor=HexColor("#1d4ed8"), spaceAfter=2),
        "MetaKey": ParagraphStyle("RMetaK", parent=base["Normal"],
                                  fontName="Helvetica-Bold", fontSize=9, leading=12,
                                  textColor=MUTED, spaceAfter=1),
        "MetaVal": ParagraphStyle("RMetaV", parent=base["Normal"],
                                  fontName="Helvetica", fontSize=10, leading=13,
                                  textColor=NAVY, spaceAfter=6),
    }


def _ts(value) -> str:
    try:
        return time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime(float(value)))
    except (ValueError, TypeError, OSError):
        return "—"


def _bullets(items: Iterable[str], style: ParagraphStyle):
    out = []
    for line in items:
        line = line.strip()
        if not line:
            continue
        out.append(Paragraph(line, style, bulletText="•"))
    return out


def _split_mitigation(text: str) -> list[str]:
    """Split mitigation text into bullet items if it looks like a numbered list,
    otherwise return it as a single paragraph."""
    lines = [l.strip() for l in (text or "").splitlines() if l.strip()]
    if not lines:
        return []
    # if any line starts with a number/bullet, treat as list
    list_like = any(l[:2].rstrip(".").isdigit() or l.startswith(("- ", "* ", "• ")) for l in lines)
    if list_like:
        # strip "1.", "2)", "-", "*", "•" prefixes
        out = []
        for l in lines:
            for prefix in ["1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.",
                           "0.", "- ", "* ", "• "]:
                if l.startswith(prefix):
                    l = l[len(prefix):].strip()
                    break
            # generic number-dot
            i = 0
            while i < len(l) and l[i].isdigit(): i += 1
            if i and i < len(l) and l[i] in ".):":
                l = l[i + 1:].strip()
            out.append(l)
        return out
    return [text.strip()]


def _footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(2 * cm, 1.2 * cm, "ThreatChain — Threat Intelligence Report")
    canvas.drawCentredString(A4[0] / 2, 1.2 * cm, f"Page {doc.page}")
    canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm,
                           time.strftime("%Y-%m-%d", time.localtime()))
    canvas.restoreState()


def build_threat_report(tx: dict, block_index: int, block_hash: str,
                        playbook: dict | None = None) -> bytes:
    """Render a single-threat PDF and return the raw bytes.

    `playbook` is the standard mitigation playbook for the threat's type,
    drawn from `mitigations.py`. If supplied, it is rendered as a separate
    'Standard Mitigation Playbook' section after the submitter's mitigation.
    """
    s = _styles()
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=1.8 * cm, bottomMargin=2 * cm,
        title=f"ThreatChain Report — {tx.get('title', '')}",
        author=tx.get("submitter_name", "ThreatChain"),
    )

    story: list = []

    # Header
    story.append(Paragraph("THREATCHAIN", s["Eyebrow"]))
    story.append(Paragraph(tx.get("title", "(untitled threat)"), s["Title"]))

    # Severity + type strip
    sev = (tx.get("severity") or "medium").lower()
    sev_color = SEVERITY_COLOR.get(sev, NAVY)
    threat_type = tx.get("threat_type", "other")
    if threat_type == "other" and tx.get("threat_type_custom"):
        threat_type = tx["threat_type_custom"]
    subtitle = (
        f"<font color='{sev_color.hexval()}'><b>{sev.upper()}</b></font> · "
        f"<b>{threat_type.upper()}</b> · "
        f"Reported by {tx.get('submitter_name', '—')} · "
        f"{_ts(tx.get('timestamp'))}"
    )
    story.append(Paragraph(subtitle, s["Subtitle"]))

    # divider rule via empty table
    rule = Table([[""]], colWidths=[17 * cm], rowHeights=[2])
    rule.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 0.5, DIVIDER)]))
    story.append(rule)
    story.append(Spacer(1, 6))

    # 1. Description
    story.append(Paragraph("1. Description", s["H2"]))
    story.append(Paragraph(tx.get("description", "(no description provided)"), s["Body"]))

    # 2. Indicators of Compromise
    iocs = tx.get("iocs") or []
    story.append(Paragraph("2. Indicators of Compromise (IOCs)", s["H2"]))
    if iocs:
        story.extend([Paragraph(i, s["Mono"], bulletText="•") for i in iocs])
    else:
        story.append(Paragraph("None provided.", s["Body"]))

    # 3. Mitigation
    story.append(Paragraph("3. Recommended Mitigation", s["H2"]))
    miti = _split_mitigation(tx.get("mitigation", ""))
    if miti:
        if len(miti) == 1:
            story.append(Paragraph(miti[0], s["Body"]))
        else:
            story.extend([Paragraph(m, s["Body"], bulletText="•") for m in miti])
    else:
        story.append(Paragraph(
            "<i>No mitigation steps were provided by the submitter. "
            "Consult internal security playbooks for this threat type.</i>",
            s["Body"]))

    # 4. Standard mitigation playbook (curated, type-based)
    if playbook:
        story.append(Paragraph(
            f"4. Standard Mitigation Playbook — {playbook.get('name', '')}",
            s["H2"]))
        if playbook.get("summary"):
            story.append(Paragraph(
                f"<i>{playbook['summary']}</i>", s["Body"]))
        for step in playbook.get("steps", []):
            story.append(Paragraph(step, s["Body"], bulletText="•"))
        refs = playbook.get("references") or []
        if refs:
            story.append(Spacer(1, 4))
            story.append(Paragraph("Authoritative references:",
                                   ParagraphStyle("RRefH", parent=s["Body"],
                                                  fontSize=9.5, textColor=MUTED,
                                                  spaceBefore=4, spaceAfter=3)))
            for r in refs:
                story.append(Paragraph(
                    f'<link href="{r["url"]}"><u>{r["name"]}</u></link>',
                    s["Link"], bulletText="•",
                ))

    # 5. Detection / Trained-model links
    links = tx.get("github_links") or []
    story.append(Paragraph("5. Detection & Trained-Model Resources", s["H2"]))
    if links:
        story.append(Paragraph(
            "<b>Submitter-provided:</b>",
            ParagraphStyle("RSubH", parent=s["Body"],
                           fontSize=9.5, textColor=MUTED, spaceAfter=3),
        ))
        for url in links:
            story.append(Paragraph(
                f'<link href="{url}"><u>{url}</u></link>',
                s["Link"], bulletText="•",
            ))

    std_models = (playbook or {}).get("detection_models") or []
    if std_models:
        label = "Standard resources for this threat type:" if links \
                else "<b>Standard resources for this threat type</b> (no submitter links were provided):"
        story.append(Spacer(1, 4))
        story.append(Paragraph(
            label,
            ParagraphStyle("RSubH2", parent=s["Body"],
                           fontSize=9.5, textColor=MUTED, spaceBefore=6, spaceAfter=4),
        ))
        for m in std_models:
            name = m.get("name", "")
            url = m.get("url", "")
            desc = m.get("description", "")
            story.append(Paragraph(
                f'<link href="{url}"><b>{name}</b></link> &nbsp;—&nbsp; '
                f'<font color="#5b6477">{desc}</font><br/>'
                f'<font color="#1d4ed8" size="8"><u>{url}</u></font>',
                ParagraphStyle("RModel", parent=s["Body"],
                               fontSize=9.5, leading=12, spaceAfter=6),
                bulletText="•",
            ))
    elif not links:
        story.append(Paragraph(
            "<i>No detection or model links available.</i>",
            s["Body"]))

    # 6. Cryptographic provenance
    story.append(Paragraph("6. Cryptographic Provenance", s["H2"]))
    sig = tx.get("signature", "")
    sig_short = sig[:48] + ("…" if len(sig) > 48 else "")
    meta_rows = [
        ["Threat ID",       tx.get("id", "—")],
        ["Submitter",       tx.get("submitter_name", "—")],
        ["Block index",     f"#{block_index}"],
        ["Block hash",      block_hash],
        ["Submitted at",    _ts(tx.get("timestamp"))],
        ["Signature (RSA-PSS-SHA256)", sig_short],
    ]
    table = Table(meta_rows, colWidths=[4.5 * cm, 12.5 * cm])
    table.setStyle(TableStyle([
        ("FONT", (0, 0), (0, -1), "Helvetica-Bold", 9),
        ("FONT", (1, 0), (1, -1), "Courier", 9),
        ("TEXTCOLOR", (0, 0), (0, -1), MUTED),
        ("TEXTCOLOR", (1, 0), (1, -1), NAVY),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("LINEBELOW", (0, 0), (-1, -1), 0.25, DIVIDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(table)

    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "<i>This document was generated from the ThreatChain ledger. "
        "The signature above can be re-verified by any peer node against "
        "the submitter's published public key. Any modification to this "
        "report after generation breaks the cryptographic link to the chain.</i>",
        ParagraphStyle("RFoot", parent=s["Body"],
                       fontSize=8.5, textColor=MUTED, alignment=TA_LEFT),
    ))

    doc.build(story, onFirstPage=_footer, onLaterPages=_footer)
    return buf.getvalue()
