import html
import io
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


INK = colors.HexColor("#172033")
MUTED = colors.HexColor("#667085")
RULE = colors.HexColor("#D9E0EA")
SOFT = colors.HexColor("#F6F8FB")
ACCENT = colors.HexColor("#2563EB")
GREEN = colors.HexColor("#0F766E")
AMBER = colors.HexColor("#B45309")
RED = colors.HexColor("#B42318")


def _clean(value):
    return html.escape(str(value or ""))


def _score(value):
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def _status_color(value):
    text = str(value or "").lower()
    if any(word in text for word in ["poor", "high", "severe", "concerning", "attention"]):
        return RED
    if any(word in text for word in ["fair", "moderate"]):
        return AMBER
    return GREEN


def _style(name, **kwargs):
    base = {
        "fontName": "Helvetica",
        "fontSize": 9,
        "leading": 13,
        "textColor": INK,
    }
    base.update(kwargs)
    return ParagraphStyle(name, **base)


def _items(values, style):
    if not values:
        return [Paragraph("No details provided.", style)]
    return [Paragraph(f"- {_clean(item)}", style) for item in values]


def generate_pdf(student_name, result):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
    )

    a1 = result.get("agent1", {})
    a2 = result.get("agent2", {})
    a3 = result.get("agent3", {})
    a4 = result.get("agent4", {})
    a5 = result.get("agent5", {})

    styles = {
        "title": _style("title", fontName="Helvetica-Bold", fontSize=18, leading=22),
        "subtitle": _style("subtitle", fontSize=9, leading=13, textColor=MUTED),
        "section": _style(
            "section",
            fontName="Helvetica-Bold",
            fontSize=9,
            leading=12,
            textColor=ACCENT,
            spaceBefore=8,
            spaceAfter=4,
        ),
        "body": _style("body", fontSize=9, leading=14),
        "small": _style("small", fontSize=8, leading=11, textColor=MUTED),
        "metric_label": _style(
            "metric_label",
            fontName="Helvetica-Bold",
            fontSize=7.5,
            leading=10,
            textColor=MUTED,
            alignment=TA_CENTER,
        ),
        "metric_value": _style(
            "metric_value",
            fontName="Helvetica-Bold",
            fontSize=20,
            leading=24,
            alignment=TA_CENTER,
        ),
        "metric_status": _style(
            "metric_status",
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=10,
            alignment=TA_CENTER,
        ),
        "footer": _style("footer", fontSize=7.5, leading=10, textColor=MUTED, alignment=TA_CENTER),
    }

    story = []
    generated = datetime.now().strftime("%d %b %Y, %I:%M %p")

    story.append(Paragraph("WellMind AI Wellness Report", styles["title"]))
    story.append(Paragraph(f"Student: {_clean(student_name)} | Generated: {generated}", styles["subtitle"]))
    story.append(Spacer(1, 5 * mm))
    story.append(HRFlowable(width="100%", color=RULE, thickness=0.8, spaceAfter=6))

    overall = a5.get("overall_status", "Pending")
    story.append(Paragraph("Overall Summary", styles["section"]))
    summary_table = Table(
        [
            [
                Paragraph("Overall status", styles["small"]),
                Paragraph(f"<b>{_clean(overall)}</b>", _style("overall", fontName="Helvetica-Bold", fontSize=10, textColor=_status_color(overall))),
            ],
            [
                Paragraph("Recommendation", styles["small"]),
                Paragraph(_clean(a5.get("summary", "No recommendation returned.")), styles["body"]),
            ],
        ],
        colWidths=[38 * mm, 132 * mm],
    )
    summary_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), SOFT),
                ("BOX", (0, 0), (-1, -1), 0.6, RULE),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, RULE),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    story.append(summary_table)
    story.append(Spacer(1, 5 * mm))

    def metric(label, score, status):
        color = _status_color(status)
        return Table(
            [
                [Paragraph(label, styles["metric_label"])],
                [Paragraph(f"{_score(score)}/100", styles["metric_value"])],
                [Paragraph(_clean(status), _style(f"{label}_status", fontName="Helvetica-Bold", fontSize=8, textColor=color, alignment=TA_CENTER))],
            ],
            colWidths=[54 * mm],
            style=TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), colors.white),
                    ("BOX", (0, 0), (-1, -1), 0.6, RULE),
                    ("TOPPADDING", (0, 0), (-1, -1), 7),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                    ("LEFTPADDING", (0, 0), (-1, -1), 6),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ]
            ),
        )

    story.append(Paragraph("Scores", styles["section"]))
    story.append(
        Table(
            [
                [
                    metric("Physical wellness", a1.get("wellness_score"), a1.get("status", "Pending")),
                    metric("Mental stress", a2.get("stress_score"), a2.get("risk_level", "Pending")),
                    metric("Academic load", a3.get("academic_load_score"), a3.get("burnout_risk", "Pending")),
                ]
            ],
            colWidths=[56 * mm, 56 * mm, 56 * mm],
            style=TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP")]),
        )
    )
    story.append(Spacer(1, 4 * mm))

    story.append(Paragraph("Priority Actions", styles["section"]))
    for index, action in enumerate(a5.get("priority_actions", []) or ["No priority actions returned."], 1):
        story.append(Paragraph(f"{index}. {_clean(action)}", styles["body"]))

    def detail_section(title, observations, actions, action_label):
        story.append(Paragraph(title, styles["section"]))
        story.append(Paragraph("Observations", _style(f"{title}_obs_title", fontName="Helvetica-Bold", fontSize=8.5)))
        story.extend(_items(observations, styles["body"]))
        story.append(Spacer(1, 1.5 * mm))
        story.append(Paragraph(action_label, _style(f"{title}_action_title", fontName="Helvetica-Bold", fontSize=8.5)))
        story.extend(_items(actions, styles["body"]))

    detail_section(
        "Physical Wellness",
        a1.get("observations", []),
        a1.get("immediate_actions", []),
        "Suggested actions",
    )
    detail_section(
        "Mental Wellness",
        a2.get("observations", []),
        a2.get("coping_recommendations", []),
        "Coping recommendations",
    )
    detail_section(
        "Academic Load",
        a3.get("observations", []),
        a3.get("study_recommendations", []),
        "Study recommendations",
    )

    if a4.get("key_takeaway") or a4.get("relevant_evidence"):
        story.append(Paragraph("Evidence Note", styles["section"]))
        if a4.get("key_takeaway"):
            story.append(Paragraph(_clean(a4.get("key_takeaway")), styles["body"]))
        story.extend(_items(a4.get("relevant_evidence", []), styles["small"]))

    story.append(Spacer(1, 5 * mm))
    story.append(HRFlowable(width="100%", color=RULE, thickness=0.6, spaceAfter=4))
    story.append(Paragraph("This report is a wellness support summary and is not a medical diagnosis.", styles["footer"]))

    doc.build(story)
    buffer.seek(0)
    return buffer
