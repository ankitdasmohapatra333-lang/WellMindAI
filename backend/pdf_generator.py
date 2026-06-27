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
SOFT_BLUE = colors.HexColor("#EDF5FF")
ACCENT = colors.HexColor("#2563EB")
GREEN = colors.HexColor("#0F766E")
GREEN_BG = colors.HexColor("#E6F6F3")
AMBER = colors.HexColor("#B45309")
AMBER_BG = colors.HexColor("#FFF4DC")
RED = colors.HexColor("#B42318")
RED_BG = colors.HexColor("#FFF0EE")
WHITE = colors.white


def _clean(value):
    return html.escape(str(value or ""))


def _score(value):
    try:
        return max(0, min(100, int(float(value))))
    except (TypeError, ValueError):
        return 0


def _style(name, **kwargs):
    base = {
        "fontName": "Helvetica",
        "fontSize": 9,
        "leading": 13,
        "textColor": INK,
    }
    base.update(kwargs)
    return ParagraphStyle(name, **base)


def _status_color(value):
    text = str(value or "").lower()
    if any(word in text for word in ["poor", "high", "severe", "concerning", "attention"]):
        return RED
    if any(word in text for word in ["fair", "moderate", "watch"]):
        return AMBER
    return GREEN


def _status_bg(value):
    color = _status_color(value)
    if color == RED:
        return RED_BG
    if color == AMBER:
        return AMBER_BG
    return GREEN_BG


def _balance_score(a1, a2, a3):
    physical = _score(a1.get("wellness_score"))
    mental_calm = 100 - _score(a2.get("stress_score"))
    academic_space = 100 - _score(a3.get("academic_load_score"))
    return round((physical + mental_calm + academic_space) / 3)


def _risk_note(a1, a2, a3, overall):
    physical = _score(a1.get("wellness_score"))
    stress = _score(a2.get("stress_score"))
    academic = _score(a3.get("academic_load_score"))
    if stress >= 75 or academic >= 75 or physical < 45:
        return (
            "Clinical watch",
            "At least one domain shows high strain. Review sleep, stress, academic pressure, and support access if symptoms continue.",
        )
    if stress >= 50 or academic >= 50 or physical < 65 or str(overall).lower() == "needs attention":
        return (
            "Preventive support",
            "Signals are not critical, but early support is recommended to prevent fatigue, stress build-up, or academic overload.",
        )
    return (
        "Stable routine",
        "Current indicators are steady. Maintain consistent sleep, hydration, movement, and planned study blocks.",
    )


def _items(values, style):
    values = values or []
    if not values:
        return [Paragraph("- No details provided.", style)]
    return [Paragraph(f"- {_clean(item)}", style) for item in values]


def _draw_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.5)
    canvas.line(doc.leftMargin, 13 * mm, A4[0] - doc.rightMargin, 13 * mm)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(doc.leftMargin, 8 * mm, "WellMind AI wellness support report - not a medical diagnosis.")
    canvas.drawRightString(A4[0] - doc.rightMargin, 8 * mm, f"Page {doc.page}")
    canvas.restoreState()


def generate_pdf(student_name, result):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=16 * mm,
        rightMargin=16 * mm,
        topMargin=14 * mm,
        bottomMargin=18 * mm,
    )

    a1 = result.get("agent1", {})
    a2 = result.get("agent2", {})
    a3 = result.get("agent3", {})
    a4 = result.get("agent4", {})
    a5 = result.get("agent5", {})

    styles = {
        "title": _style("title", fontName="Helvetica-Bold", fontSize=18, leading=22),
        "subtitle": _style("subtitle", fontSize=8.5, leading=12, textColor=MUTED),
        "section": _style(
            "section",
            fontName="Helvetica-Bold",
            fontSize=9,
            leading=12,
            textColor=ACCENT,
            spaceBefore=8,
            spaceAfter=4,
        ),
        "body": _style("body", fontSize=8.8, leading=13),
        "small": _style("small", fontSize=7.7, leading=10.5, textColor=MUTED),
        "label": _style("label", fontName="Helvetica-Bold", fontSize=7.5, leading=10, textColor=MUTED),
        "metric_label": _style(
            "metric_label",
            fontName="Helvetica-Bold",
            fontSize=7.2,
            leading=9,
            textColor=MUTED,
            alignment=TA_CENTER,
        ),
        "metric_value": _style(
            "metric_value",
            fontName="Helvetica-Bold",
            fontSize=18,
            leading=22,
            alignment=TA_CENTER,
        ),
    }

    generated = datetime.now().strftime("%d %b %Y, %I:%M %p")
    overall = a5.get("overall_status", "Pending")
    balance = _balance_score(a1, a2, a3)
    risk_label, risk_text = _risk_note(a1, a2, a3, overall)

    story = []

    header = Table(
        [
            [
                Paragraph("WellMind AI", _style("brand", fontName="Helvetica-Bold", fontSize=10, textColor=ACCENT)),
                Paragraph("Wellness Review Report", styles["title"]),
            ],
            [
                Paragraph("Student wellness support summary", styles["subtitle"]),
                Paragraph(f"Student: <b>{_clean(student_name)}</b><br/>Generated: {_clean(generated)}", styles["subtitle"]),
            ],
        ],
        colWidths=[42 * mm, 121 * mm],
    )
    header.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    story.append(header)
    story.append(Spacer(1, 3 * mm))
    story.append(HRFlowable(width="100%", color=RULE, thickness=0.8, spaceAfter=5))

    snapshot = Table(
        [
            [
                Paragraph("Overall status", styles["label"]),
                Paragraph("Balance score", styles["label"]),
                Paragraph("Review level", styles["label"]),
            ],
            [
                Paragraph(f"<b>{_clean(overall)}</b>", _style("overall_value", fontName="Helvetica-Bold", fontSize=12, textColor=_status_color(overall))),
                Paragraph(f"<b>{balance}/100</b>", _style("balance_value", fontName="Helvetica-Bold", fontSize=12, textColor=INK)),
                Paragraph(f"<b>{_clean(risk_label)}</b>", _style("risk_value", fontName="Helvetica-Bold", fontSize=12, textColor=_status_color(risk_label))),
            ],
            [
                Paragraph(_clean(a5.get("summary", "No summary returned.")), styles["body"]),
                Paragraph("Integrated from physical wellness, mental stress, and academic load indicators.", styles["small"]),
                Paragraph(_clean(risk_text), styles["body"]),
            ],
        ],
        colWidths=[55 * mm, 49 * mm, 59 * mm],
    )
    snapshot.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), SOFT),
                ("BOX", (0, 0), (-1, -1), 0.7, RULE),
                ("INNERGRID", (0, 0), (-1, -1), 0.35, RULE),
                ("SPAN", (0, 2), (0, 2)),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    story.append(snapshot)
    story.append(Spacer(1, 4 * mm))

    def metric_card(label, score, status, note):
        status_text = _clean(status)
        return Table(
            [
                [Paragraph(label, styles["metric_label"])],
                [Paragraph(f"{_score(score)}/100", styles["metric_value"])],
                [Paragraph(f"<b>{status_text}</b>", _style(f"{label}_status", fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=_status_color(status), alignment=TA_CENTER))],
                [Paragraph(_clean(note), styles["small"])],
            ],
            colWidths=[52 * mm],
            style=TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), WHITE),
                    ("BACKGROUND", (0, 2), (-1, 2), _status_bg(status)),
                    ("BOX", (0, 0), (-1, -1), 0.6, RULE),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                    ("LEFTPADDING", (0, 0), (-1, -1), 7),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ]
            ),
        )

    story.append(Paragraph("Domain Scores", styles["section"]))
    story.append(
        Table(
            [
                [
                    metric_card("Physical Wellness", a1.get("wellness_score"), a1.get("status", "Pending"), (a1.get("observations") or [""])[0]),
                    metric_card("Mental Stress", a2.get("stress_score"), a2.get("risk_level", "Pending"), (a2.get("observations") or [""])[0]),
                    metric_card("Academic Load", a3.get("academic_load_score"), a3.get("burnout_risk", "Pending"), (a3.get("observations") or [""])[0]),
                ]
            ],
            colWidths=[54.3 * mm, 54.3 * mm, 54.3 * mm],
            style=TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP")]),
        )
    )
    story.append(Spacer(1, 3 * mm))

    story.append(Paragraph("Recommended Follow-up", styles["section"]))
    actions = a5.get("priority_actions", []) or ["Continue monitoring wellness indicators and repeat the check-in tomorrow."]
    story.append(
        Table(
            [[Paragraph(f"{idx}. {_clean(action)}", styles["body"])] for idx, action in enumerate(actions[:4], 1)],
            colWidths=[163 * mm],
            style=TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), SOFT_BLUE),
                    ("BOX", (0, 0), (-1, -1), 0.6, RULE),
                    ("TOPPADDING", (0, 0), (-1, -1), 5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                    ("LEFTPADDING", (0, 0), (-1, -1), 8),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ]
            ),
        )
    )

    if a5.get("escalation_recommended"):
        story.append(Spacer(1, 2 * mm))
        story.append(
            Paragraph(
                f"<b>Support flag:</b> {_clean(a5.get('escalation_reason', 'Additional support is recommended.'))}",
                _style("support_flag", fontSize=8.8, leading=13, textColor=RED),
            )
        )

    def detail_section(title, score_line, observations, actions, action_label):
        rows = [
            [Paragraph("Current signal", styles["label"]), Paragraph(_clean(score_line), styles["body"])],
            [Paragraph("Observations", styles["label"]), _items(observations, styles["body"])],
            [Paragraph(action_label, styles["label"]), _items(actions, styles["body"])],
        ]
        table = Table(rows, colWidths=[34 * mm, 129 * mm])
        table.setStyle(
            TableStyle(
                [
                    ("BOX", (0, 0), (-1, -1), 0.5, RULE),
                    ("INNERGRID", (0, 0), (-1, -1), 0.3, RULE),
                    ("BACKGROUND", (0, 0), (0, -1), SOFT),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                    ("LEFTPADDING", (0, 0), (-1, -1), 7),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ]
            )
        )
        story.append(Paragraph(title, styles["section"]))
        story.append(table)

    detail_section(
        "Physical Review",
        f"{_score(a1.get('wellness_score'))}/100 - {a1.get('status', 'Pending')}",
        a1.get("observations", []),
        a1.get("immediate_actions", []),
        "Care actions",
    )
    detail_section(
        "Mental Stress Review",
        f"{_score(a2.get('stress_score'))}/100 - {a2.get('risk_level', 'Pending')}",
        a2.get("observations", []),
        a2.get("coping_recommendations", []),
        "Coping plan",
    )
    detail_section(
        "Academic Load Review",
        f"{_score(a3.get('academic_load_score'))}/100 - {a3.get('burnout_risk', 'Pending')}",
        a3.get("observations", []),
        a3.get("study_recommendations", []),
        "Load plan",
    )

    if a4.get("key_takeaway") or a4.get("relevant_evidence"):
        story.append(Paragraph("Evidence Note", styles["section"]))
        evidence_rows = []
        if a4.get("key_takeaway"):
            evidence_rows.append([Paragraph("Takeaway", styles["label"]), Paragraph(_clean(a4.get("key_takeaway")), styles["body"])])
        evidence = a4.get("relevant_evidence", []) or []
        if evidence:
            evidence_rows.append([Paragraph("Grounding", styles["label"]), _items(evidence[:3], styles["small"])])
        evidence_table = Table(evidence_rows, colWidths=[34 * mm, 129 * mm])
        evidence_table.setStyle(
            TableStyle(
                [
                    ("BOX", (0, 0), (-1, -1), 0.5, RULE),
                    ("INNERGRID", (0, 0), (-1, -1), 0.3, RULE),
                    ("BACKGROUND", (0, 0), (0, -1), SOFT),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                    ("LEFTPADDING", (0, 0), (-1, -1), 7),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ]
            )
        )
        story.append(evidence_table)

    story.append(Spacer(1, 4 * mm))
    story.append(
        Paragraph(
            "Clinical note: This report summarizes self-reported wellness inputs and AI-assisted interpretation. It can support a conversation with a doctor, counselor, mentor, or caregiver, but it does not diagnose or replace professional care.",
            styles["small"],
        )
    )

    doc.build(story, onFirstPage=_draw_footer, onLaterPages=_draw_footer)
    buffer.seek(0)
    return buffer
