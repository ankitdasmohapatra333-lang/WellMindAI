"""WellMind AI - Plotly Chart Components"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

BG = "rgba(0,0,0,0)"
GRID = "rgba(255,255,255,0.05)"
TEXT = "#94A3B8"
PRIMARY = "#00E5B0"
SECONDARY = "#5EEAD4"
PURPLE = "#8B5CF6"
PINK = "#EC4899"
ORANGE = "#F59E0B"


def _base_layout(**kwargs):
    base = dict(
        paper_bgcolor=BG,
        plot_bgcolor=BG,
        font=dict(family="Inter, sans-serif", color=TEXT, size=12),
        showlegend=kwargs.get("showlegend", False),
    )
    # Allow callers to override any key, including margin
    extra = {k: v for k, v in kwargs.items() if k != "showlegend"}
    base.update(extra)
    # Set default margin only if not already provided
    base.setdefault("margin", dict(l=10, r=10, t=30, b=10))
    return base


def wellness_gauge(score: float, grade: str):
    color = PRIMARY if score >= 70 else ORANGE if score >= 50 else "#EF4444"
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={"font": {"size": 48, "color": color, "family": "Space Grotesk"}, "suffix": ""},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": TEXT, "tickfont": {"size": 10}},
            "bar": {"color": color, "thickness": 0.25},
            "bgcolor": "rgba(15,29,45,0.5)",
            "bordercolor": "rgba(0,229,176,0.2)",
            "steps": [
                {"range": [0, 50], "color": "rgba(239,68,68,0.15)"},
                {"range": [50, 70], "color": "rgba(245,158,11,0.15)"},
                {"range": [70, 100], "color": "rgba(0,229,176,0.15)"},
            ],
            "threshold": {"line": {"color": color, "width": 3}, "thickness": 0.8, "value": score},
        },
        title={"text": f"<b>Grade {grade}</b>", "font": {"size": 16, "color": color}},
    ))
    fig.update_layout(**_base_layout(margin=dict(l=20, r=20, t=40, b=10)), height=260)
    return fig


def burnout_donut(risk: float):
    safe = 100 - risk
    color = PRIMARY if risk < 25 else ORANGE if risk < 50 else "#F97316" if risk < 75 else "#EF4444"
    fig = go.Figure(go.Pie(
        values=[risk, safe],
        labels=["Risk", "Safe"],
        hole=0.72,
        marker_colors=[color, "rgba(255,255,255,0.05)"],
        textinfo="none",
        hoverinfo="label+percent",
    ))
    fig.add_annotation(
        text=f"<b>{risk:.0f}%</b>",
        x=0.5, y=0.55,
        font=dict(size=28, color=color, family="Space Grotesk"),
        showarrow=False,
    )
    fig.add_annotation(
        text="Burnout Risk",
        x=0.5, y=0.38,
        font=dict(size=11, color=TEXT),
        showarrow=False,
    )
    fig.update_layout(**_base_layout(margin=dict(l=10, r=10, t=10, b=10)), height=220)
    return fig


def stress_bar(stress_level: str):
    levels = ["Low", "Moderate", "High", "Severe"]
    colors_map = {"Low": PRIMARY, "Moderate": ORANGE, "High": "#F97316", "Severe": "#EF4444"}
    color = colors_map.get(stress_level, PRIMARY)

    values = [100 if l == stress_level else 20 for l in levels]
    bar_colors = [color if l == stress_level else "rgba(255,255,255,0.06)" for l in levels]

    fig = go.Figure(go.Bar(
        x=levels, y=values,
        marker_color=bar_colors,
        text=["✓" if l == stress_level else "" for l in levels],
        textposition="outside",
        textfont=dict(color=color, size=14),
    ))
    fig.update_layout(
        **_base_layout(),
        height=200,
        yaxis=dict(visible=False, range=[0, 130]),
        xaxis=dict(tickfont=dict(color=TEXT)),
        bargap=0.35,
    )
    return fig


def wellness_trend(df: pd.DataFrame):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["Date"], y=df["Wellness Score"],
        mode="lines+markers",
        line=dict(color=PRIMARY, width=2.5, shape="spline"),
        marker=dict(size=7, color=PRIMARY, line=dict(color="white", width=1.5)),
        fill="tozeroy",
        fillcolor="rgba(0,229,176,0.08)",
        name="Wellness Score",
    ))
    fig.update_layout(
        **_base_layout(showlegend=False),
        height=220,
        xaxis=dict(gridcolor=GRID, tickfont=dict(color=TEXT)),
        yaxis=dict(gridcolor=GRID, tickfont=dict(color=TEXT), range=[0, 100]),
        title=dict(text="Wellness Score — 7 Day Trend", font=dict(color=TEXT, size=13), x=0.02),
    )
    return fig


def sleep_stress_chart(df: pd.DataFrame):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df["Date"], y=df["Sleep Hours"],
        name="Sleep (hrs)",
        marker_color="rgba(94,234,212,0.8)",
        yaxis="y",
    ))
    fig.add_trace(go.Scatter(
        x=df["Date"], y=df["Stress Level"],
        name="Stress (1-10)",
        line=dict(color=ORANGE, width=2.5),
        marker=dict(size=6, color=ORANGE),
        mode="lines+markers",
        yaxis="y2",
    ))
    fig.update_layout(
        **_base_layout(showlegend=True),
        height=240,
        legend=dict(orientation="h", y=-0.2, font=dict(color=TEXT)),
        xaxis=dict(gridcolor=GRID, tickfont=dict(color=TEXT)),
        yaxis=dict(gridcolor=GRID, tickfont=dict(color=TEXT), title="Sleep hrs", titlefont=dict(color=SECONDARY)),
        yaxis2=dict(overlaying="y", side="right", tickfont=dict(color=ORANGE), title="Stress", titlefont=dict(color=ORANGE)),
        title=dict(text="Sleep vs Stress Correlation", font=dict(color=TEXT, size=13), x=0.02),
        barmode="group",
    )
    return fig


def burnout_trend(df: pd.DataFrame):
    colors = [PRIMARY if v < 40 else ORANGE if v < 65 else "#EF4444" for v in df["Burnout Risk"]]
    fig = go.Figure(go.Bar(
        x=df["Date"], y=df["Burnout Risk"],
        marker_color=colors,
        text=[f"{v}%" for v in df["Burnout Risk"]],
        textposition="outside",
        textfont=dict(color=TEXT, size=10),
    ))
    fig.add_hline(y=50, line_dash="dash", line_color=ORANGE, annotation_text="Risk Threshold", annotation_font_color=ORANGE)
    fig.update_layout(
        **_base_layout(),
        height=230,
        xaxis=dict(gridcolor=GRID, tickfont=dict(color=TEXT)),
        yaxis=dict(gridcolor=GRID, tickfont=dict(color=TEXT), range=[0, 110]),
        title=dict(text="Burnout Risk — 7 Days (%)", font=dict(color=TEXT, size=13), x=0.02),
    )
    return fig


def study_area_chart(df: pd.DataFrame):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["Date"], y=df["Study Hours"],
        mode="lines+markers",
        line=dict(color=PURPLE, width=2.5, shape="spline"),
        marker=dict(size=7, color=PURPLE),
        fill="tozeroy",
        fillcolor="rgba(139,92,246,0.1)",
        name="Study Hours",
    ))
    fig.add_hline(y=6, line_dash="dot", line_color=ORANGE, annotation_text="Optimal Max", annotation_font_color=ORANGE)
    fig.update_layout(
        **_base_layout(),
        height=220,
        xaxis=dict(gridcolor=GRID, tickfont=dict(color=TEXT)),
        yaxis=dict(gridcolor=GRID, tickfont=dict(color=TEXT)),
        title=dict(text="Study Hours — Weekly Pattern", font=dict(color=TEXT, size=13), x=0.02),
    )
    return fig
