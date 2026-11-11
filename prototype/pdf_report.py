"""
pdf_report.py — simple black-and-white per-threat PDF report.
"""

from __future__ import annotations
import io
from datetime import datetime, timezone
from typing import Any

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)

BLACK  = colors.HexColor("#111111")
GRAY   = colors.HexColor("#555555")
LGRAY  = colors.HexColor("#AAAAAA")
WHITE  = colors.white


def _styles():
    return {
        "h1": ParagraphStyle("h1",
            fontName="Helvetica-Bold", fontSize=18, textColor=BLACK,
            leading=24, spaceAfter=4),
        "h2": ParagraphStyle("h2",
            fontName="Helvetica-Bold", fontSize=11, textColor=BLACK,
            leading=15, spaceBefore=14, spaceAfter=4),
        "body": ParagraphStyle("body",
            fontName="Helvetica", fontSize=10, textColor=BLACK,
            leading=15, spaceAfter=3),
        "meta": ParagraphStyle("meta",
            fontName="Helvetica", fontSize=9, textColor=GRAY,
            leading=13),
        "mono": ParagraphStyle("mono",
            fontName="Courier", fontSize=9, textColor=BLACK,
            leading=13, spaceAfter=2),
        "mono_gray": ParagraphStyle("mono_gray",
            fontName="Courier", fontSize=8, textColor=GRAY,
            leading=12),
        "footer": ParagraphStyle("footer",
            fontName="Helvetica", fontSize=8, textColor=LGRAY,
            alignment=TA_CENTER, leading=11),
    }


def _ioc_list(iocs) -> list[str]:
    if not iocs:
        return []
    if isinstance(iocs, list):
        return [str(i).strip() for i in iocs if str(i).strip()]
    return [line.strip() for line in str(iocs).splitlines() if line.strip()]


def build_threat_report(tx: dict[str, Any],
                        block_index: int,
                        block_hash: str,
                        playbook: dict[str, Any] | None = None) -> bytes:

    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=20*mm, rightMargin=20*mm,
        topMargin=18*mm, bottomMargin=18*mm,
    )

    st  = _styles()
    W   = A4[0] - 40*mm
    els = []

    # ── meta info ─────────────────────────────────────────────────────────────
    threat_type = (tx.get("threat_type_custom") or tx.get("threat_type") or "Unknown").upper()
    severity    = (tx.get("severity") or "Unknown").upper()
    title_text  = tx.get("title") or "Threat Report"
    org_name    = tx.get("submitter_name") or "Unknown Organisation"

    ts = tx.get("timestamp")
    date_str = (datetime.fromtimestamp(float(ts), tz=timezone.utc)
                .strftime("%d %b %Y  %H:%M UTC")) if ts else "Unknown date"

    # ── title ─────────────────────────────────────────────────────────────────
    els.append(Paragraph("ThreatChain — Threat Report", st["meta"]))
    els.append(Spacer(1, 3))
    els.append(Paragraph(title_text, st["h1"]))
    els.append(HRFlowable(width=W, thickness=1.5, color=BLACK))
    els.append(Spacer(1, 6))

    # ── quick-info row ────────────────────────────────────────────────────────
    info = [["Type", "Severity", "Submitted by", "Date"],
            [threat_type, severity, org_name, date_str]]
    info_tbl = Table(info, colWidths=[W*0.18, W*0.14, W*0.36, W*0.32])
    info_tbl.setStyle(TableStyle([
        ("FONTNAME",  (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME",  (0, 1), (-1, 1), "Helvetica"),
        ("FONTSIZE",  (0, 0), (-1, -1), 9),
        ("TEXTCOLOR", (0, 0), (-1, 0), GRAY),
        ("TEXTCOLOR", (0, 1), (-1, 1), BLACK),
        ("TOPPADDING",    (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LINEBELOW", (0, 0), (-1, 0), 0.5, LGRAY),
        ("LINEBELOW", (0, 1), (-1, 1), 0.5, LGRAY),
    ]))
    els.append(info_tbl)
    els.append(Spacer(1, 10))

    # ── 1. Description ────────────────────────────────────────────────────────
    els.append(Paragraph("1.  Description", st["h2"]))
    els.append(HRFlowable(width=W, thickness=0.5, color=LGRAY))
    els.append(Spacer(1, 4))
    desc = (tx.get("description") or "No description provided.").strip()
    els.append(Paragraph(desc.replace("\n", "<br/>"), st["body"]))
    els.append(Spacer(1, 6))

    # ── 2. Indicators of Compromise ──────────────────────────────────────────
    iocs = _ioc_list(tx.get("iocs"))
    if iocs:
        els.append(Paragraph("2.  Indicators of Compromise (IOCs)", st["h2"]))
        els.append(HRFlowable(width=W, thickness=0.5, color=LGRAY))
        els.append(Spacer(1, 4))
        for ioc in iocs:
            els.append(Paragraph(f"•   {ioc}", st["mono"]))
        els.append(Spacer(1, 6))

    # ── 3. Submitter Mitigation ───────────────────────────────────────────────
    mitigation = (tx.get("mitigation") or "").strip()
    if mitigation:
        els.append(Paragraph("3.  Submitter Mitigation Guidance", st["h2"]))
        els.append(HRFlowable(width=W, thickness=0.5, color=LGRAY))
        els.append(Spacer(1, 4))
        els.append(Paragraph(mitigation.replace("\n", "<br/>"), st["body"]))
        els.append(Spacer(1, 6))

    # ── 4. Standard Mitigation Playbook ──────────────────────────────────────
    if playbook:
        steps = playbook.get("steps") or []
        refs  = playbook.get("references") or []
        if steps:
            els.append(Paragraph("4.  Standard Mitigation Playbook", st["h2"]))
            els.append(HRFlowable(width=W, thickness=0.5, color=LGRAY))
            els.append(Spacer(1, 4))
            for i, step in enumerate(steps, 1):
                els.append(Paragraph(f"{i}.  {step}", st["body"]))
            if refs:
                els.append(Spacer(1, 4))
                for ref in refs:
                    els.append(Paragraph(f"•   {ref}", st["mono_gray"]))
            els.append(Spacer(1, 6))

    # ── 5. Detection Resources ────────────────────────────────────────────────
    github_links = tx.get("github_links") or []
    if isinstance(github_links, str):
        github_links = [l.strip() for l in github_links.splitlines() if l.strip()]
    if github_links:
        els.append(Paragraph("5.  Detection Resources", st["h2"]))
        els.append(HRFlowable(width=W, thickness=0.5, color=LGRAY))
        els.append(Spacer(1, 4))
        for link in github_links:
            els.append(Paragraph(f"•   {link}", st["mono_gray"]))
        els.append(Spacer(1, 6))

    # ── 6. Cryptographic Provenance ───────────────────────────────────────────
    els.append(Paragraph("6.  Cryptographic Provenance", st["h2"]))
    els.append(HRFlowable(width=W, thickness=0.5, color=LGRAY))
    els.append(Spacer(1, 4))

    sig         = tx.get("signature", "")
    sig_preview = sig[:64] + "…" if len(sig) > 64 else sig
    pub_key     = (tx.get("submitter_pub") or "")
    pub_preview = pub_key[:64] + "…" if len(pub_key) > 64 else pub_key

    prov = [
        ["Block Index",      str(block_index)],
        ["Block Hash",       block_hash or "N/A"],
        ["Transaction ID",   tx.get("id", "N/A")],
        ["Submitter Key",    pub_preview],
        ["Signature",        sig_preview],
    ]
    prov_tbl = Table(prov, colWidths=[W*0.22, W*0.78])
    prov_tbl.setStyle(TableStyle([
        ("FONTNAME",  (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME",  (1, 0), (1, -1), "Courier"),
        ("FONTSIZE",  (0, 0), (-1, -1), 8),
        ("TEXTCOLOR", (0, 0), (0, -1), GRAY),
        ("TEXTCOLOR", (1, 0), (1, -1), BLACK),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 4),
        ("LINEBELOW", (0, 0), (-1, -2), 0.4, LGRAY),
    ]))
    els.append(prov_tbl)
    els.append(Spacer(1, 12))
    els.append(HRFlowable(width=W, thickness=0.5, color=LGRAY))
    els.append(Spacer(1, 4))
    els.append(Paragraph(
        f"Verify this report: fetch Block #{block_index} from any ThreatChain node "
        "and confirm the block hash and signature match the values above.",
        st["footer"]
    ))

    doc.build(els)
    return buf.getvalue()
