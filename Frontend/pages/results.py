"""WellMind AI - Results Dashboard"""
import streamlit as st
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from components.cards import section_header, kpi_card, recommendation_card, evidence_card
from components.animations import glowing_divider
from components.charts import wellness_gauge, burnout_donut, stress_bar
from utils.helpers import get_grade, get_burnout_label, get_stress_label


def render():
    result = st.session_state.get("analysis_result")

    if not result:
        st.markdown("""
        <div class="glass-card" style="text-align:center; padding:3rem;">
            <div style="font-size:3rem; margin-bottom:1rem;">📊</div>
            <div style="font-size:1.1rem; color:#94A3B8;">No results yet. Run an assessment first.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("← Start Assessment"):
            st.session_state["page"] = "Assessment"
            st.rerun()
        return

    score = result["wellness_score"]
    grade, grade_color = get_grade(score)
    burnout = result["burnout_risk"]
    burnout_label, burnout_color = get_burnout_label(burnout)
    stress_color, _ = get_stress_label(result["stress_level"])

    st.markdown("""
    <div class="page-hero fade-up">
        <h1>📊 Wellness Results Dashboard</h1>
        <p>AI-generated analysis based on your 5-agent assessment. Updated in real time.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI Row ───────────────────────────────────────────────────────────────
    section_header("🎯", "Key Wellness Indicators")
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    with kpi1:
        kpi_card("🏆", str(score), "Wellness Score", grade_color)
    with kpi2:
        kpi_card("📝", grade, "Wellness Grade", grade_color)
    with kpi3:
        kpi_card("💪", result["physical_status"], "Physical Status",
                 "#00E5B0" if result["physical_status"] in ["Excellent","Good"] else "#F59E0B")
    with kpi4:
        kpi_card("🧠", result["stress_level"], "Stress Class", stress_color)
    with kpi5:
        kpi_card("🔥", f"{burnout}%", "Burnout Risk", burnout_color)

    glowing_divider()

    # ── Charts Row ────────────────────────────────────────────────────────────
    section_header("📈", "Visual Analytics")
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown('<div style="font-size:0.78rem; color:#94A3B8; text-transform:uppercase; letter-spacing:1px; margin-bottom:4px; text-align:center;">Wellness Gauge</div>', unsafe_allow_html=True)
        st.plotly_chart(wellness_gauge(score, grade), width="stretch", config={"displayModeBar": False})

    with c2:
        st.markdown('<div style="font-size:0.78rem; color:#94A3B8; text-transform:uppercase; letter-spacing:1px; margin-bottom:4px; text-align:center;">Burnout Risk Meter</div>', unsafe_allow_html=True)
        st.plotly_chart(burnout_donut(burnout), width="stretch", config={"displayModeBar": False})
        st.markdown(f'<div style="text-align:center; color:{burnout_color}; font-weight:600; font-size:0.85rem; margin-top:-1rem;">{burnout_label}</div>', unsafe_allow_html=True)

    with c3:
        st.markdown('<div style="font-size:0.78rem; color:#94A3B8; text-transform:uppercase; letter-spacing:1px; margin-bottom:4px; text-align:center;">Stress Classification</div>', unsafe_allow_html=True)
        st.plotly_chart(stress_bar(result["stress_level"]), width="stretch", config={"displayModeBar": False})

    glowing_divider()

    # ── Physical Metrics Detail ───────────────────────────────────────────────
    section_header("💪", "Detailed Metrics")
    data = st.session_state.get("assessment_data", {})

    m1, m2, m3, m4, m5 = st.columns(5)
    metrics = [
        ("🌙", "Sleep", f"{data.get('sleep_hours',0)}h", 7, 9, "hrs"),
        ("💧", "Hydration", f"{data.get('water_intake',0)} gl", 6, 8, "glasses"),
        ("📚", "Study Load", f"{data.get('study_hours',0)}h", 0, 6, "hrs"),
        ("🏃", "Exercise", f"{data.get('exercise_minutes',0)}m", 20, 45, "min"),
        ("😊", "Mood", data.get('mood','—'), None, None, ""),
    ]
    for col, (icon, label, val, lo, hi, unit) in zip([m1, m2, m3, m4, m5], metrics):
        with col:
            if lo is not None:
                raw = float(str(val).replace("h","").replace("gl","").replace("m","").strip() or 0)
                pct = min(100, max(0, (raw / hi) * 100)) if hi else 0
                bar_color = "#00E5B0" if raw >= lo else "#F59E0B" if raw >= lo * 0.7 else "#EF4444"
                st.markdown(f"""
                <div class="glass-card" style="text-align:center; padding:1rem;">
                    <div style="font-size:1.5rem;">{icon}</div>
                    <div style="font-size:1.2rem; font-weight:700; color:{bar_color}; font-family:'Space Grotesk',sans-serif;">{val}</div>
                    <div style="font-size:0.72rem; color:#94A3B8; margin-bottom:0.5rem;">{label}</div>
                    <div class="progress-wrap">
                        <div class="progress-fill" style="width:{pct}%; background:{bar_color};"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                mood_colors = {"Excellent":"#00E5B0","Good":"#5EEAD4","Neutral":"#94A3B8","Tired":"#F59E0B","Stressed":"#EF4444"}
                mc = mood_colors.get(val, "#94A3B8")
                st.markdown(f"""
                <div class="glass-card" style="text-align:center; padding:1rem;">
                    <div style="font-size:1.5rem;">{icon}</div>
                    <div style="font-size:1.1rem; font-weight:700; color:{mc}; font-family:'Space Grotesk',sans-serif;">{val}</div>
                    <div style="font-size:0.72rem; color:#94A3B8;">{label}</div>
                </div>
                """, unsafe_allow_html=True)

    glowing_divider()

    # ── Recommendations & Evidence ────────────────────────────────────────────
    rec_col, ev_col = st.columns([1, 1])
    with rec_col:
        section_header("✨", f"Recommendations ({len(result['recommendations'])})")
        for rec in result["recommendations"]:
            recommendation_card(rec["icon"], rec["title"], rec["desc"], rec["priority"])
    with ev_col:
        section_header("🔍", f"Evidence Base ({len(result['evidence'])})")
        for ev in result["evidence"]:
            evidence_card(ev["source"], ev["finding"], ev["relevance"])

    glowing_divider()

    # ── PDF Download ──────────────────────────────────────────────────────────
    section_header("📄", "Export Report")
    col_dl, col_info = st.columns([1, 2])
    with col_dl:
        pdf_bytes = _generate_pdf(result, data)
        st.download_button(
            label="⬇️  Download PDF Report",
            data=pdf_bytes,
            file_name="wellmind_wellness_report.pdf",
            mime="application/pdf",
            width="stretch",
        )
    with col_info:
        st.markdown(f"""
        <div style="color:#94A3B8; font-size:0.85rem; padding-top:0.4rem;">
            Report includes wellness score, stress analysis, burnout risk, personalized recommendations, and evidence sources.
            <br><span style="color:#00E5B0; font-weight:600;">Wellness Score: {score}/100 · Grade: {grade}</span>
        </div>
        """, unsafe_allow_html=True)


def _generate_pdf(result: dict, data: dict) -> bytes:
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=20*mm, rightMargin=20*mm,
        topMargin=18*mm, bottomMargin=18*mm,
    )

    # ── Colours ───────────────────────────────────────────────────────────────
    TEAL   = colors.HexColor("#00E5B0")
    DARK   = colors.HexColor("#07131F")
    SLATE  = colors.HexColor("#94A3B8")
    WHITE  = colors.white
    AMBER  = colors.HexColor("#F59E0B")
    RED    = colors.HexColor("#EF4444")
    PURPLE = colors.HexColor("#8B5CF6")

    grade, _ = get_grade(result["wellness_score"])
    score_val = result["wellness_score"]
    score_color = TEAL if score_val >= 70 else AMBER if score_val >= 50 else RED

    # ── Styles ────────────────────────────────────────────────────────────────
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("title", fontSize=22, textColor=TEAL,
                                  fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=4)
    sub_style   = ParagraphStyle("sub", fontSize=10, textColor=SLATE,
                                  fontName="Helvetica", alignment=TA_CENTER, spaceAfter=14)
    h2_style    = ParagraphStyle("h2", fontSize=13, textColor=TEAL,
                                  fontName="Helvetica-Bold", spaceBefore=12, spaceAfter=6)
    body_style  = ParagraphStyle("body", fontSize=9.5, textColor=colors.HexColor("#CBD5E1"),
                                  fontName="Helvetica", spaceAfter=4, leading=14)
    label_style = ParagraphStyle("label", fontSize=8.5, textColor=SLATE,
                                  fontName="Helvetica-Bold", spaceAfter=2)

    story = []

    # ── Header ────────────────────────────────────────────────────────────────
    story.append(Paragraph("WellMind AI", title_style))
    story.append(Paragraph("AI-Powered Student Wellness Report", sub_style))
    story.append(HRFlowable(width="100%", thickness=1, color=TEAL, spaceAfter=10))

    # ── Score Banner ──────────────────────────────────────────────────────────
    banner_data = [[
        Paragraph(f'<font color="#07131F" size="28"><b>{score_val}</b></font>', ParagraphStyle("s", alignment=TA_CENTER, fontName="Helvetica-Bold")),
        Paragraph(f'<font color="#07131F" size="18"><b>Grade {grade}</b></font>', ParagraphStyle("g", alignment=TA_CENTER, fontName="Helvetica-Bold")),
        Paragraph(f'<font color="#07131F" size="11">{result.get("physical_status","—")}<br/>Physical Status</font>', ParagraphStyle("p", alignment=TA_CENTER, fontName="Helvetica")),
        Paragraph(f'<font color="#07131F" size="11">{result.get("stress_level","—")}<br/>Stress Class</font>', ParagraphStyle("p2", alignment=TA_CENTER, fontName="Helvetica")),
        Paragraph(f'<font color="#07131F" size="11">{result.get("burnout_risk","—")}%<br/>Burnout Risk</font>', ParagraphStyle("p3", alignment=TA_CENTER, fontName="Helvetica")),
    ]]
    banner = Table(banner_data, colWidths=[35*mm]*5)
    banner.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), TEAL),
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [TEAL]),
        ("BOX", (0,0), (-1,-1), 0.5, DARK),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("ROUNDEDCORNERS", [6]),
    ]))
    story.append(banner)
    story.append(Spacer(1, 10*mm))

    # ── Assessment Inputs ─────────────────────────────────────────────────────
    story.append(Paragraph("Assessment Inputs", h2_style))
    story.append(HRFlowable(width="100%", thickness=0.4, color=SLATE, spaceAfter=6))
    input_rows = [
        ["Sleep Hours", f"{data.get('sleep_hours','N/A')} hrs", "Water Intake", f"{data.get('water_intake','N/A')} glasses"],
        ["Stress Level", f"{data.get('stress_level','N/A')} / 10", "Study Hours", f"{data.get('study_hours','N/A')} hrs"],
        ["Exercise", f"{data.get('exercise_minutes','N/A')} min", "Mood", data.get('mood','N/A')],
    ]
    cell_style = ParagraphStyle("cell", fontSize=9, textColor=colors.HexColor("#CBD5E1"), fontName="Helvetica")
    cell_label = ParagraphStyle("clabel", fontSize=9, textColor=SLATE, fontName="Helvetica-Bold")
    tbl_data = [[Paragraph(r[0], cell_label), Paragraph(r[1], cell_style),
                 Paragraph(r[2], cell_label), Paragraph(r[3], cell_style)] for r in input_rows]
    tbl = Table(tbl_data, colWidths=[42*mm, 48*mm, 42*mm, 43*mm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#0F1D2D")),
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [colors.HexColor("#0F1D2D"), colors.HexColor("#0A1624")]),
        ("BOX", (0,0), (-1,-1), 0.5, colors.HexColor("#1E3A4A")),
        ("INNERGRID", (0,0), (-1,-1), 0.3, colors.HexColor("#1E3A4A")),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
    ]))
    story.append(tbl)
    story.append(Spacer(1, 8*mm))

    # ── Recommendations ───────────────────────────────────────────────────────
    story.append(Paragraph("Personalized Recommendations", h2_style))
    story.append(HRFlowable(width="100%", thickness=0.4, color=SLATE, spaceAfter=6))
    priority_color = {"High": RED, "Medium": AMBER, "Low": TEAL}
    for rec in result.get("recommendations", []):
        pc = priority_color.get(rec.get("priority","Low"), TEAL)
        rec_row = [[
            Paragraph(f'<font color="{pc.hexval() if hasattr(pc,"hexval") else "#00E5B0"}">[{rec.get("priority","—")}]</font>', ParagraphStyle("pri", fontSize=8, fontName="Helvetica-Bold")),
            Paragraph(f'<b>{rec.get("icon","")} {rec.get("title","")}</b><br/><font color="#94A3B8">{rec.get("desc","")}</font>', body_style),
        ]]
        rt = Table(rec_row, colWidths=[18*mm, 157*mm])
        rt.setStyle(TableStyle([
            ("VALIGN", (0,0), (-1,-1), "TOP"),
            ("TOPPADDING", (0,0), (-1,-1), 4),
            ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ]))
        story.append(rt)
    story.append(Spacer(1, 6*mm))

    # ── Evidence ──────────────────────────────────────────────────────────────
    story.append(Paragraph("Evidence Base", h2_style))
    story.append(HRFlowable(width="100%", thickness=0.4, color=SLATE, spaceAfter=6))
    for ev in result.get("evidence", []):
        story.append(Paragraph(f'<b>{ev.get("source","")}</b> — Relevance: {ev.get("relevance","")}%', label_style))
        story.append(Paragraph(ev.get("finding",""), body_style))

    # ── Footer ────────────────────────────────────────────────────────────────
    story.append(Spacer(1, 8*mm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=TEAL, spaceAfter=4))
    story.append(Paragraph("Generated by WellMind AI · 5-Agent Wellness Analysis System", sub_style))

    doc.build(story)
    return buf.getvalue()
