import html
import importlib
import os
import sys
import threading
import time as _time
from datetime import datetime, timedelta

import pandas as pd
import requests
import streamlit as st


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

API_URL = os.getenv("WELLMIND_API_URL", "http://127.0.0.1:8000")
PAGES = ["Daily Check-In", "Dashboard", "History"]


st.set_page_config(
    page_title="WellMind AI",
    page_icon="WM",
    layout="wide",
    initial_sidebar_state="expanded",
)


DEFAULTS = {
    "page": "Daily Check-In",
    "theme": "light",
    "student_name": "",
    "currentStudent": "",
    "result": None,
    "result_name": "",
    "weekly_plan": None,
    "pdf_bytes": None,
    "pdf_error": None,
    "isPdfReady": False,
    "last_saved_id": None,
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

if st.session_state.page == "Weekly Plan":
    st.session_state.page = "Dashboard"


def palette():
    if st.session_state.theme == "dark":
        return {
            "bg": "#0F172A",
            "panel": "#1E293B",
            "panel_soft": "#263449",
            "ink": "#F1F5F9",
            "muted": "#94A3B8",
            "quiet": "#CBD5E1",
            "line": "#334155",
            "accent": "#38BDF8",
            "accent_soft": "#0B3B52",
            "mint": "#5EEAD4",
            "mint_soft": "#103F39",
            "amber": "#FCD34D",
            "amber_soft": "#473715",
            "red": "#FCA5A5",
            "red_soft": "#4A2428",
            "recommend_bg": "#172033",
            "sidebar": "#0F172A",
            "button_text": "#08111E",
            "input_bg": "#0F172A",
            "shadow": "0 18px 42px rgba(0,0,0,.28)",
        }

    return {
        "bg": "#FFFFFF",
        "panel": "#FFFFFF",
        "panel_soft": "#F8FAFC",
        "ink": "#111827",
        "muted": "#6B7280",
        "quiet": "#64748B",
        "line": "#E5E7EB",
        "accent": "#2563EB",
        "accent_soft": "#EFF6FF",
        "mint": "#0F766E",
        "mint_soft": "#E6F6F3",
        "amber": "#B45309",
        "amber_soft": "#FFF4DC",
        "red": "#B42318",
        "red_soft": "#FFF0EE",
        "recommend_bg": "#FBFDFF",
        "sidebar": "#FFFFFF",
        "button_text": "#FFFFFF",
        "input_bg": "#FFFFFF",
        "shadow": "0 14px 36px rgba(15,23,42,.08)",
    }


C = palette()

st.markdown(
    f"""
<style>
:root {{
    --bg: {C["bg"]};
    --panel: {C["panel"]};
    --panel-soft: {C["panel_soft"]};
    --ink: {C["ink"]};
    --muted: {C["muted"]};
    --quiet: {C["quiet"]};
    --line: {C["line"]};
    --accent: {C["accent"]};
    --accent-soft: {C["accent_soft"]};
    --mint: {C["mint"]};
    --mint-soft: {C["mint_soft"]};
    --amber: {C["amber"]};
    --amber-soft: {C["amber_soft"]};
    --red: {C["red"]};
    --red-soft: {C["red_soft"]};
    --recommend-bg: {C["recommend_bg"]};
    --button-text: {C["button_text"]};
    --input-bg: {C["input_bg"]};
    --shadow: {C["shadow"]};
}}

html, body, [class*="css"] {{
    font-family: Inter, "Segoe UI", system-ui, -apple-system, sans-serif;
    color: var(--ink);
    transition: background-color 180ms ease, color 180ms ease;
}}

.stApp {{
    background: var(--bg);
    color: var(--ink);
    transition: background-color 180ms ease, color 180ms ease;
}}

.block-container {{
    max-width: 1220px;
    padding-top: 3.25rem;
    padding-bottom: 2rem;
}}

[data-testid="stHeader"] {{
    background: var(--bg);
    border-bottom: 1px solid var(--line);
}}

[data-testid="stSidebar"] {{
    background: {C["sidebar"]};
    border-right: 1px solid var(--line);
    box-shadow: 8px 0 28px rgba(15, 23, 42, .04);
}}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] label {{
    color: var(--muted);
}}

[data-testid="stSidebar"] .stRadio > div {{
    gap: .7rem;
}}

[data-testid="stSidebar"] .stRadio {{
    margin: 2.4rem 0 3rem;
}}

[data-testid="stSidebar"] .stRadio label {{
    min-height: 3rem;
    padding: .75rem .85rem;
    border-radius: 12px;
    border: 1px solid transparent;
    color: var(--muted);
    font-size: 1.02rem;
    font-weight: 650;
    transition: background-color 180ms ease, color 180ms ease, border-color 180ms ease, transform 180ms ease;
}}

[data-testid="stSidebar"] .stRadio label:hover {{
    background: var(--panel-soft);
    border-color: var(--line);
    color: var(--ink);
    transform: translateX(2px);
}}

[data-testid="stSidebar"] .stRadio label:has(input:checked) {{
    background: var(--accent-soft);
    border-color: var(--accent);
    color: var(--accent);
}}

.wm-brand {{
    padding: .25rem 0 1.1rem;
}}

.wm-mark {{
    width: 38px;
    height: 38px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 8px;
    background: var(--ink);
    color: var(--bg);
    font-size: .78rem;
    font-weight: 800;
    margin-right: .65rem;
}}

.wm-brand-title {{
    display: inline-block;
    vertical-align: middle;
    line-height: 1.15;
    font-size: 1rem;
    font-weight: 750;
    color: var(--ink);
}}

.wm-brand-sub {{
    display: block;
    margin-top: .16rem;
    font-size: .68rem;
    font-weight: 600;
    letter-spacing: .06em;
    text-transform: uppercase;
    color: var(--quiet);
}}

.sidebar-section-title {{
    color: var(--quiet);
    font-size: .72rem;
    font-weight: 800;
    letter-spacing: .08em;
    text-transform: uppercase;
    margin: .4rem 0 .7rem;
}}

.sidebar-bottom-panel {{
    background: var(--panel-soft);
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: .85rem;
    margin-top: .5rem;
}}

.sidebar-student {{
    color: var(--ink);
    font-weight: 750;
    margin-bottom: .35rem;
}}

.wm-hero {{
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 14px;
    box-shadow: var(--shadow);
    padding: 1.35rem 1.5rem;
    margin-bottom: 1.3rem;
}}

.download-panel {{
    background: var(--panel-soft);
    border: 1px solid var(--line);
    border-radius: 8px;
    padding: .75rem;
    margin-top: .45rem;
}}

.wm-hero-row {{
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    gap: 1rem;
}}

.wm-kicker {{
    color: var(--accent);
    font-size: .72rem;
    font-weight: 760;
    letter-spacing: .08em;
    text-transform: uppercase;
    margin-bottom: .35rem;
}}

.wm-title {{
    font-size: 1.72rem;
    font-weight: 780;
    letter-spacing: 0;
    color: var(--ink);
    margin: 0;
}}

.wm-subtitle {{
    color: var(--muted);
    font-size: .92rem;
    margin-top: .35rem;
}}

.wm-meta {{
    color: var(--quiet);
    font-size: .78rem;
    text-align: right;
    white-space: nowrap;
}}

.section-title {{
    color: var(--ink);
    font-size: .84rem;
    font-weight: 760;
    letter-spacing: .05em;
    text-transform: uppercase;
    margin: 1.1rem 0 .65rem;
}}

.soft-panel,
.dashboard-card,
.metric-card,
.history-item {{
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 14px;
    box-shadow: var(--shadow);
    transition: background-color 180ms ease, border-color 180ms ease, box-shadow 180ms ease;
}}

.soft-panel {{
    padding: 1rem;
}}

.dashboard-card {{
    padding: 1rem;
    min-height: 132px;
}}

.dashboard-card .label {{
    color: var(--muted);
    font-size: .73rem;
    font-weight: 760;
    letter-spacing: .06em;
    text-transform: uppercase;
}}

.dashboard-card .big {{
    color: var(--ink);
    font-size: 1.7rem;
    line-height: 1.1;
    font-weight: 820;
    margin-top: .55rem;
}}

.dashboard-card .note {{
    color: var(--muted);
    font-size: .82rem;
    line-height: 1.45;
    margin-top: .55rem;
}}

.metric-card {{
    padding: 1rem;
    min-height: 146px;
}}

.metric-top {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: .7rem;
}}

.metric-label {{
    font-size: .74rem;
    font-weight: 760;
    letter-spacing: .06em;
    text-transform: uppercase;
    color: var(--muted);
}}

.metric-value {{
    margin-top: .55rem;
    font-size: 2rem;
    line-height: 1;
    font-weight: 800;
    color: var(--ink);
}}

.metric-note {{
    margin-top: .55rem;
    font-size: .82rem;
    line-height: 1.45;
    color: var(--muted);
}}

.badge {{
    display: inline-flex;
    align-items: center;
    border-radius: 999px;
    padding: .22rem .55rem;
    font-size: .72rem;
    font-weight: 720;
    white-space: nowrap;
}}

.badge.good {{
    color: var(--mint);
    background: var(--mint-soft);
}}

.badge.warn {{
    color: var(--amber);
    background: var(--amber-soft);
}}

.badge.risk {{
    color: var(--red);
    background: var(--red-soft);
}}

.recommendation {{
    border: 1px solid var(--line);
    border-left: 4px solid var(--accent);
    background: var(--recommend-bg);
    border-radius: 14px;
    box-shadow: var(--shadow);
    padding: 1rem 1.1rem;
    margin: .8rem 0 1rem;
}}

.recommendation-title {{
    color: var(--accent);
    font-size: .76rem;
    font-weight: 780;
    letter-spacing: .07em;
    text-transform: uppercase;
    margin-bottom: .45rem;
}}

.recommendation-body {{
    color: var(--ink);
    font-size: .96rem;
    line-height: 1.55;
}}

.action-row {{
    display: flex;
    gap: .75rem;
    align-items: flex-start;
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 14px;
    box-shadow: var(--shadow);
    padding: .75rem .85rem;
    margin-bottom: .5rem;
}}

.action-index {{
    width: 1.55rem;
    height: 1.55rem;
    border-radius: 999px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: var(--accent-soft);
    color: var(--accent);
    font-size: .78rem;
    font-weight: 800;
    flex: 0 0 auto;
}}

.action-text {{
    color: var(--ink);
    font-size: .9rem;
    line-height: 1.45;
}}

.tiny {{
    color: var(--quiet);
    font-size: .76rem;
}}

.history-item {{
    padding: .8rem .9rem;
    margin-bottom: .55rem;
}}

.score-row {{
    display: grid;
    grid-template-columns: 120px minmax(0, 1fr) 56px;
    align-items: center;
    gap: .75rem;
    margin: .75rem 0;
}}

.score-row .name {{
    color: var(--muted);
    font-size: .82rem;
    font-weight: 680;
}}

.bar {{
    height: 9px;
    border-radius: 99px;
    background: var(--panel-soft);
    overflow: hidden;
}}

.bar > span {{
    display: block;
    height: 100%;
    background: var(--accent);
    border-radius: inherit;
}}

.balance-panel {{
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 14px;
    box-shadow: var(--shadow);
    padding: .8rem 1rem;
}}

.dashboard-hero {{
    display: grid;
    grid-template-columns: minmax(0, 1.35fr) minmax(280px, .65fr);
    gap: 1rem;
    margin-bottom: 1rem;
}}

.wellness-welcome {{
    position: relative;
    overflow: hidden;
    background:
        radial-gradient(circle at 88% 12%, {"rgba(56,189,248,.24)" if st.session_state.theme == "dark" else "rgba(37,99,235,.12)"}, transparent 34%),
        linear-gradient(135deg, var(--panel), var(--panel-soft));
    border: 1px solid var(--line);
    border-radius: 22px;
    box-shadow: var(--shadow);
    padding: 1.25rem 1.35rem;
    min-height: 172px;
}}

.welcome-eyebrow {{
    color: var(--accent);
    font-size: .72rem;
    font-weight: 850;
    letter-spacing: .08em;
    text-transform: uppercase;
}}

.welcome-title {{
    color: var(--ink);
    font-size: 2rem;
    font-weight: 850;
    letter-spacing: 0;
    margin-top: .35rem;
}}

.welcome-copy {{
    color: var(--muted);
    font-size: .94rem;
    max-width: 640px;
    line-height: 1.55;
    margin-top: .45rem;
}}

.wellness-pills {{
    display: flex;
    flex-wrap: wrap;
    gap: .45rem;
    margin-top: 1rem;
}}

.wellness-pill {{
    background: var(--accent-soft);
    color: var(--accent);
    border: 1px solid {"rgba(56,189,248,.38)" if st.session_state.theme == "dark" else "rgba(37,99,235,.18)"};
    border-radius: 999px;
    padding: .34rem .7rem;
    font-size: .76rem;
    font-weight: 780;
}}

.calendar-panel {{
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 22px;
    box-shadow: var(--shadow);
    padding: 1rem;
}}

.calendar-title {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: var(--ink);
    font-weight: 820;
    margin-bottom: .85rem;
}}

.calendar-title span {{
    color: var(--muted);
    font-size: .76rem;
    font-weight: 700;
}}

.calendar-strip {{
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: .42rem;
}}

.calendar-day {{
    text-align: center;
    border-radius: 14px;
    padding: .55rem .25rem;
    background: var(--panel-soft);
    border: 1px solid transparent;
}}

.calendar-day strong {{
    display: block;
    color: var(--ink);
    font-size: .86rem;
    margin-top: .18rem;
}}

.calendar-day span {{
    color: var(--muted);
    font-size: .64rem;
    font-weight: 760;
    text-transform: uppercase;
}}

.calendar-day.active {{
    background: var(--accent);
    border-color: var(--accent);
}}

.calendar-day.active strong,
.calendar-day.active span {{
    color: var(--button-text);
}}

.activity-grid {{
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 1rem;
    margin-bottom: 1rem;
}}

.activity-card {{
    position: relative;
    overflow: hidden;
    border-radius: 22px;
    padding: 1rem;
    min-height: 142px;
    box-shadow: var(--shadow);
    color: #ffffff;
}}

.activity-card:after {{
    content: "";
    position: absolute;
    width: 130px;
    height: 130px;
    right: -48px;
    top: -44px;
    border-radius: 999px;
    background: rgba(255,255,255,.18);
}}

.activity-icon {{
    width: 38px;
    height: 38px;
    border-radius: 14px;
    background: rgba(255,255,255,.22);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 900;
    margin-bottom: .95rem;
}}

.activity-label {{
    font-size: .77rem;
    font-weight: 760;
    opacity: .84;
}}

.activity-value {{
    font-size: 1.85rem;
    font-weight: 900;
    line-height: 1;
    margin-top: .32rem;
}}

.activity-note {{
    font-size: .75rem;
    opacity: .86;
    margin-top: .48rem;
}}

.activity-blue {{ background: linear-gradient(135deg, #38BDF8, #2563EB); }}
.activity-green {{ background: linear-gradient(135deg, #34D399, #0F766E); }}
.activity-violet {{ background: linear-gradient(135deg, #A78BFA, #6D28D9); }}
.activity-indigo {{ background: linear-gradient(135deg, #60A5FA, #4F46E5); }}

.dashboard-main-grid {{
    display: grid;
    grid-template-columns: minmax(0, 1.1fr) minmax(300px, .9fr);
    gap: 1rem;
}}

.premium-panel {{
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 22px;
    box-shadow: var(--shadow);
    padding: 1rem;
}}

.panel-title-row {{
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    align-items: center;
    margin-bottom: .85rem;
}}

.panel-title-row strong {{
    color: var(--ink);
    font-size: 1rem;
}}

.soft-chart {{
    height: 170px;
    border-radius: 18px;
    background:
        linear-gradient(180deg, {"rgba(56,189,248,.22)" if st.session_state.theme == "dark" else "rgba(14,165,233,.18)"}, transparent),
        var(--panel-soft);
    border: 1px solid var(--line);
    position: relative;
    overflow: hidden;
    margin-top: .85rem;
}}

.soft-chart svg {{
    width: 100%;
    height: 100%;
}}

.week-focus-grid {{
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: .75rem;
    margin: .85rem 0 1rem;
}}

.focus-card {{
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 18px;
    box-shadow: var(--shadow);
    padding: .85rem;
}}

.focus-card span {{
    display: block;
    color: var(--accent);
    font-size: .68rem;
    font-weight: 850;
    text-transform: uppercase;
    letter-spacing: .06em;
    margin-bottom: .25rem;
}}

.focus-card strong {{
    color: var(--ink);
    font-size: .9rem;
}}

.clinical-grid {{
    display: grid;
    grid-template-columns: minmax(0, 1.05fr) minmax(300px, .95fr);
    gap: 1rem;
    margin-top: .35rem;
}}

.clinical-list {{
    display: grid;
    gap: .55rem;
    margin-top: .7rem;
}}

.clinical-row {{
    display: grid;
    grid-template-columns: 112px minmax(0, 1fr);
    gap: .7rem;
    align-items: start;
    padding: .7rem 0;
    border-top: 1px solid var(--line);
}}

.clinical-row:first-child {{
    border-top: 0;
    padding-top: 0;
}}

.clinical-row .row-label {{
    color: var(--muted);
    font-size: .72rem;
    font-weight: 820;
    letter-spacing: .06em;
    text-transform: uppercase;
}}

.clinical-row .row-body {{
    color: var(--ink);
    font-size: .88rem;
    line-height: 1.45;
}}

.review-strip {{
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: .6rem;
    margin-top: .8rem;
}}

.review-chip {{
    border: 1px solid var(--line);
    background: var(--panel-soft);
    border-radius: 12px;
    padding: .65rem;
    min-height: 72px;
}}

.review-chip span {{
    display: block;
    color: var(--muted);
    font-size: .66rem;
    font-weight: 820;
    letter-spacing: .06em;
    text-transform: uppercase;
    margin-bottom: .28rem;
}}

.review-chip strong {{
    color: var(--ink);
    font-size: .95rem;
    line-height: 1.2;
}}

.priority-stack {{
    display: grid;
    gap: .6rem;
}}

.weekly-grid {{
    display: grid;
    grid-template-columns: repeat(7, minmax(220px, 1fr));
    gap: .9rem;
    overflow-x: auto;
    padding: .15rem .05rem .45rem;
}}

.day-card {{
    min-width: 220px;
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 18px;
    box-shadow: var(--shadow);
    padding: .85rem;
}}

.day-name {{
    color: var(--ink);
    font-size: .98rem;
    font-weight: 800;
}}

.day-sub {{
    color: var(--muted);
    font-size: .72rem;
    font-weight: 700;
    margin-top: .15rem;
}}

.day-head {{
    display: flex;
    justify-content: space-between;
    gap: .6rem;
    align-items: flex-start;
    margin-bottom: .75rem;
}}

.day-count {{
    background: var(--accent-soft);
    color: var(--accent);
    border-radius: 999px;
    padding: .2rem .48rem;
    font-size: .68rem;
    font-weight: 820;
    white-space: nowrap;
}}

.plan-track {{
    display: grid;
    gap: .48rem;
}}

.plan-item {{
    display: grid;
    grid-template-columns: 28px minmax(0, 1fr);
    gap: .55rem;
    align-items: start;
    border-radius: 12px;
    border: 1px solid transparent;
    padding: .58rem .62rem;
    font-size: .78rem;
    line-height: 1.35;
}}

.plan-item .time {{
    display: block;
    color: var(--quiet);
    font-size: .66rem;
    font-weight: 820;
    letter-spacing: .02em;
    margin-bottom: .12rem;
}}

.plan-icon {{
    width: 28px;
    height: 28px;
    border-radius: 9px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: rgba(255,255,255,.48);
    font-size: .78rem;
    font-weight: 900;
}}

.plan-copy {{
    min-width: 0;
}}

.plan-title {{
    color: inherit;
    font-size: .82rem;
    font-weight: 760;
    overflow-wrap: anywhere;
}}

.plan-item.sleep {{ background: {"#172B42" if st.session_state.theme == "dark" else "#ECF5FF"}; border-color: {"#1E4D71" if st.session_state.theme == "dark" else "#BAE6FD"}; color: {"#BAE6FD" if st.session_state.theme == "dark" else "#075985"}; }}
.plan-item.study {{ background: {"#202449" if st.session_state.theme == "dark" else "#EEF2FF"}; border-color: {"#373B73" if st.session_state.theme == "dark" else "#C7D2FE"}; color: {"#C7D2FE" if st.session_state.theme == "dark" else "#3730A3"}; }}
.plan-item.food {{ background: {"#3A2A12" if st.session_state.theme == "dark" else "#FFF7E6"}; border-color: {"#6E5118" if st.session_state.theme == "dark" else "#FDE68A"}; color: {"#FCD34D" if st.session_state.theme == "dark" else "#92400E"}; }}
.plan-item.move {{ background: {"#17351F" if st.session_state.theme == "dark" else "#E9F8EF"}; border-color: {"#236A35" if st.session_state.theme == "dark" else "#BBF7D0"}; color: {"#BBF7D0" if st.session_state.theme == "dark" else "#166534"}; }}
.plan-item.calm {{ background: {"#123831" if st.session_state.theme == "dark" else "#EEFCF8"}; border-color: {"#1C685D" if st.session_state.theme == "dark" else "#99F6E4"}; color: {"#99F6E4" if st.session_state.theme == "dark" else "#0F766E"}; }}
.plan-item.free {{ background: var(--panel-soft); border-color: var(--line); color: var(--muted); }}

.plan-dashboard {{
    display: grid;
    grid-template-columns: minmax(0, 1fr) minmax(280px, .72fr);
    gap: 1rem;
    margin: .75rem 0 1rem;
}}

.plan-legend {{
    display: flex;
    flex-wrap: wrap;
    gap: .45rem;
    margin-top: .75rem;
}}

.legend-pill {{
    display: inline-flex;
    align-items: center;
    gap: .34rem;
    border: 1px solid var(--line);
    background: var(--panel-soft);
    color: var(--muted);
    border-radius: 999px;
    padding: .32rem .58rem;
    font-size: .73rem;
    font-weight: 760;
}}

.routine-list {{
    display: grid;
    gap: .5rem;
    margin-top: .65rem;
}}

.routine-row {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: .75rem;
    border-top: 1px solid var(--line);
    padding-top: .55rem;
    color: var(--ink);
    font-size: .82rem;
}}

.routine-row:first-child {{
    border-top: 0;
    padding-top: 0;
}}

.routine-row span {{
    color: var(--muted);
    font-size: .72rem;
    font-weight: 820;
    letter-spacing: .05em;
    text-transform: uppercase;
}}

.timeline {{
    overflow-x: auto;
    border: 1px solid var(--line);
    border-radius: 14px;
    background: var(--panel);
}}

.plan-table {{
    width: 100%;
    border-collapse: collapse;
    min-width: 920px;
}}

.plan-table th {{
    background: var(--panel-soft);
    color: var(--muted);
    font-size: .72rem;
    text-transform: uppercase;
    letter-spacing: .06em;
    padding: .65rem .55rem;
    border-bottom: 1px solid var(--line);
    text-align: left;
}}

.plan-table td {{
    border-bottom: 1px solid var(--line);
    border-right: 1px solid var(--line);
    padding: .55rem;
    vertical-align: top;
    color: var(--ink);
    font-size: .78rem;
}}

.plan-table tr:last-child td {{
    border-bottom: 0;
}}

.slot {{
    border-radius: 6px;
    padding: .36rem .42rem;
    min-height: 2.15rem;
    line-height: 1.25;
}}

.slot.sleep {{ background: {"#172B42" if st.session_state.theme == "dark" else "#ECF5FF"}; color: {"#BAE6FD" if st.session_state.theme == "dark" else "#075985"}; }}
.slot.study {{ background: {"#202449" if st.session_state.theme == "dark" else "#EEF2FF"}; color: {"#C7D2FE" if st.session_state.theme == "dark" else "#3730A3"}; }}
.slot.food {{ background: {"#3A2A12" if st.session_state.theme == "dark" else "#FFF7E6"}; color: {"#FCD34D" if st.session_state.theme == "dark" else "#92400E"}; }}
.slot.move {{ background: {"#17351F" if st.session_state.theme == "dark" else "#E9F8EF"}; color: {"#BBF7D0" if st.session_state.theme == "dark" else "#166534"}; }}
.slot.calm {{ background: {"#123831" if st.session_state.theme == "dark" else "#EEFCF8"}; color: {"#99F6E4" if st.session_state.theme == "dark" else "#0F766E"}; }}
.slot.free {{ background: var(--panel-soft); color: var(--muted); }}

[data-testid="stMetricValue"] {{
    font-size: 1.7rem;
}}

.stButton > button,
.stDownloadButton > button {{
    border-radius: 12px;
    border: 1px solid var(--line);
    box-shadow: none;
    min-height: 2.65rem;
    font-weight: 700;
    transition: background-color 180ms ease, color 180ms ease, border-color 180ms ease, transform 180ms ease;
}}

.stButton > button:hover,
.stDownloadButton > button:hover {{
    transform: translateY(-1px);
    border-color: var(--accent);
}}

.stButton > button[kind="primary"] {{
    background: var(--accent);
    border-color: var(--accent);
    color: var(--button-text);
}}

div[data-testid="stForm"] {{
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 1rem;
    background: var(--panel);
    box-shadow: var(--shadow);
}}

input, textarea, [data-baseweb="select"] > div {{
    background: var(--input-bg);
    color: var(--ink) !important;
    border-color: var(--line) !important;
}}

[data-baseweb="select"] span,
[data-baseweb="select"] input {{
    color: var(--ink) !important;
}}

[data-baseweb="slider"] [role="slider"] {{
    background: var(--accent) !important;
    border: 2px solid var(--panel) !important;
    box-shadow: 0 0 0 4px var(--accent-soft) !important;
}}

[data-baseweb="slider"] div {{
    transition: background-color 180ms ease, box-shadow 180ms ease;
}}

label, p, span, [data-testid="stMarkdownContainer"] {{
    color: inherit;
}}

[data-testid="stTextInput"] input {{
    color: var(--ink);
    background: var(--input-bg);
}}

[data-testid="stAlert"] {{
    border-radius: 8px;
}}

.progress-container {{
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 14px;
    box-shadow: var(--shadow);
    padding: 1.25rem 1.35rem;
    margin: 1rem 0;
}}

.progress-title {{
    color: var(--ink);
    font-size: 1rem;
    font-weight: 780;
    margin-bottom: .85rem;
}}

.progress-bar-track {{
    width: 100%;
    height: 8px;
    background: var(--panel-soft);
    border-radius: 99px;
    overflow: hidden;
    margin-bottom: 1rem;
}}

.progress-bar-fill {{
    height: 100%;
    background: linear-gradient(90deg, var(--accent), {"#5EEAD4" if st.session_state.theme == "dark" else "#0F766E"});
    border-radius: inherit;
    transition: width 400ms cubic-bezier(.4, 0, .2, 1);
}}

.progress-steps {{
    display: flex;
    flex-direction: column;
    gap: .45rem;
}}

.progress-step {{
    display: flex;
    align-items: center;
    gap: .6rem;
    font-size: .88rem;
    color: var(--muted);
    transition: color 180ms ease;
}}

.progress-step.done {{
    color: {"#5EEAD4" if st.session_state.theme == "dark" else "#0F766E"};
    font-weight: 680;
}}

.progress-step.running {{
    color: var(--accent);
    font-weight: 700;
}}

.progress-step .step-icon {{
    width: 22px;
    height: 22px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 999px;
    font-size: .72rem;
    font-weight: 800;
    flex: 0 0 auto;
}}

.progress-step.done .step-icon {{
    background: {"#103F39" if st.session_state.theme == "dark" else "#E6F6F3"};
    color: {"#5EEAD4" if st.session_state.theme == "dark" else "#0F766E"};
}}

.progress-step.running .step-icon {{
    background: var(--accent-soft);
    color: var(--accent);
}}

.progress-step.pending .step-icon {{
    background: var(--panel-soft);
    color: var(--muted);
    border: 1px solid var(--line);
}}

.progress-percent {{
    color: var(--muted);
    font-size: .78rem;
    font-weight: 700;
    text-align: right;
    margin-bottom: .35rem;
}}

.quota-card {{
    background: var(--panel);
    border: 1px solid {"#4A2428" if st.session_state.theme == "dark" else "#FCA5A5"};
    border-left: 4px solid {"#FCA5A5" if st.session_state.theme == "dark" else "#B42318"};
    border-radius: 14px;
    box-shadow: var(--shadow);
    padding: 1.15rem 1.25rem;
    margin: 1rem 0;
}}

.quota-title {{
    color: {"#FCA5A5" if st.session_state.theme == "dark" else "#B42318"};
    font-size: .88rem;
    font-weight: 780;
    margin-bottom: .45rem;
}}

.quota-body {{
    color: var(--muted);
    font-size: .9rem;
    line-height: 1.55;
}}

.provider-toast {{
    background: var(--panel);
    border: 1px solid {"rgba(56,189,248,.38)" if st.session_state.theme == "dark" else "rgba(37,99,235,.18)"};
    border-left: 4px solid var(--accent);
    border-radius: 14px;
    box-shadow: var(--shadow);
    padding: 1rem 1.15rem;
    margin: .75rem 0;
    display: flex;
    align-items: center;
    gap: .75rem;
}}

.provider-toast .toast-icon {{
    width: 32px;
    height: 32px;
    border-radius: 10px;
    background: var(--accent-soft);
    color: var(--accent);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: .9rem;
    font-weight: 800;
    flex: 0 0 auto;
}}

.provider-toast .toast-text {{
    color: var(--ink);
    font-size: .88rem;
    font-weight: 650;
    line-height: 1.45;
}}

.provider-toast .toast-sub {{
    color: var(--muted);
    font-size: .78rem;
    font-weight: 600;
}}

@media (max-width: 900px) {{
    .wm-hero-row {{
        display: block;
    }}
    .wm-meta {{
        margin-top: .75rem;
        text-align: left;
    }}
    .score-row {{
        grid-template-columns: 1fr;
        gap: .35rem;
    }}
    .plan-dashboard,
    .clinical-grid {{
        grid-template-columns: 1fr;
    }}
    .weekly-grid {{
        grid-template-columns: repeat(7, minmax(210px, 1fr));
    }}
    .review-strip {{
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }}
}}
</style>
""",
    unsafe_allow_html=True,
)


def esc(value):
    return html.escape(str(value or ""))


def status_kind(value):
    value = str(value or "").lower()
    if any(word in value for word in ["poor", "high", "severe", "concerning", "attention"]):
        return "risk"
    if any(word in value for word in ["fair", "moderate"]):
        return "warn"
    return "good"


def first_text(items, fallback="No detail available yet."):
    if isinstance(items, list) and items:
        return items[0]
    return fallback


def safe_number(value, default=0):
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def clamp_score(value):
    return max(0, min(100, safe_number(value)))


def render_header(title, subtitle, kicker="Wellness workspace"):
    now = datetime.now().strftime("%d %b %Y")
    active = st.session_state.currentStudent or st.session_state.result_name or "No active student"
    _, theme_col = st.columns([7.2, 1.15])
    with theme_col:
        dark_mode = st.toggle(
            "Dark mode",
            value=st.session_state.theme == "dark",
            key=f"theme_toggle_{title}",
        )
        next_theme = "dark" if dark_mode else "light"
        if next_theme != st.session_state.theme:
            st.session_state.theme = next_theme
            st.rerun()

    st.markdown(
        f"""
<div class="wm-hero">
    <div class="wm-hero-row">
        <div>
            <div class="wm-kicker">{esc(kicker)}</div>
            <h1 class="wm-title">{esc(title)}</h1>
            <div class="wm-subtitle">{esc(subtitle)}</div>
        </div>
        <div class="wm-meta">{esc(active)}<br>{now}</div>
    </div>
</div>
""",
        unsafe_allow_html=True,
    )


def section(title):
    st.markdown(f'<div class="section-title">{esc(title)}</div>', unsafe_allow_html=True)


def score_card(label, score, status, note):
    kind = status_kind(status)
    st.markdown(
        f"""
<div class="metric-card">
    <div class="metric-top">
        <div class="metric-label">{esc(label)}</div>
        <div class="badge {kind}">{esc(status or "Pending")}</div>
    </div>
    <div class="metric-value">{safe_number(score)}/100</div>
    <div class="metric-note">{esc(note)}</div>
</div>
""",
        unsafe_allow_html=True,
    )


def dashboard_card(label, value, note, badge=None):
    badge_html = f'<span class="badge {status_kind(badge)}">{esc(badge)}</span>' if badge else ""
    badge_cell = f"<div>{badge_html}</div>" if badge_html else "<div></div>"
    st.markdown(
        f"""
<div class="dashboard-card">
    <div class="metric-top">
        <div class="label">{esc(label)}</div>
        {badge_cell}
    </div>
    <div class="big">{esc(value)}</div>
    <div class="note">{esc(note)}</div>
</div>
""",
        unsafe_allow_html=True,
    )


def render_score_bar(name, value):
    value = clamp_score(value)
    st.markdown(
        score_bar_html(name, value),
        unsafe_allow_html=True,
    )


def score_bar_html(name, value):
    value = clamp_score(value)
    return f"""
<div class="score-row">
    <div class="name">{esc(name)}</div>
    <div class="bar"><span style="width:{value}%"></span></div>
    <div class="tiny">{value}/100</div>
</div>
"""


def activity_card_html(label, value, note, icon, color_class):
    return f"""
<div class="activity-card {color_class}">
    <div class="activity-icon">{esc(icon)}</div>
    <div class="activity-label">{esc(label)}</div>
    <div class="activity-value">{esc(value)}</div>
    <div class="activity-note">{esc(note)}</div>
</div>
"""


def calendar_strip_html():
    today = datetime.now()
    start = today - timedelta(days=3)
    cells = []
    for index in range(7):
        day = start + timedelta(days=index)
        active = " active" if day.date() == today.date() else ""
        cells.append(
            f"""
<div class="calendar-day{active}">
    <span>{day.strftime('%a')}</span>
    <strong>{day.day}</strong>
</div>
"""
        )

    return f"""
<div class="calendar-panel">
    <div class="calendar-title">
        Calendar
        <span>{today.strftime('%B %Y')}</span>
    </div>
    <div class="calendar-strip">{"".join(cells)}</div>
</div>
"""


def chart_svg_html(physical_score, stress_score, academic_score, balance_score):
    points = [
        (6, 108 - physical_score * .72),
        (28, 118 - (100 - stress_score) * .7),
        (52, 112 - balance_score * .72),
        (76, 116 - (100 - academic_score) * .7),
        (96, 108 - max(balance_score, physical_score) * .72),
    ]
    path = " ".join(
        [f"{'M' if idx == 0 else 'L'} {x:.1f} {max(18, min(92, y)):.1f}" for idx, (x, y) in enumerate(points)]
    )
    return f"""
<div class="soft-chart">
    <svg viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">
        <path d="M 0 100 L {path[2:]} L 100 100 Z" fill="rgba(56,189,248,.14)"></path>
        <path d="{path}" fill="none" stroke="var(--accent)" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"></path>
        <circle cx="{points[2][0]}" cy="{max(18, min(92, points[2][1]))}" r="2.7" fill="var(--accent)"></circle>
    </svg>
</div>
"""


def score_signal(value, reverse=False):
    value = clamp_score(value)
    if reverse:
        if value >= 75:
            return "High watch"
        if value >= 45:
            return "Monitor"
        return "Low watch"
    if value >= 75:
        return "Strong"
    if value >= 55:
        return "Watch"
    return "Needs support"


def risk_interpretation(overall, physical_score, stress_score, academic_score, balance_score):
    if stress_score >= 75 or academic_score >= 75 or physical_score < 45:
        level = "Clinical watch"
        note = "The report shows at least one high-pressure domain. Prioritize recovery, reduce load where possible, and consider a support check-in if symptoms persist."
    elif stress_score >= 50 or academic_score >= 50 or physical_score < 65:
        level = "Preventive support"
        note = "The report is not critical, but there are early signals worth addressing today so stress and fatigue do not accumulate."
    else:
        level = "Stable routine"
        note = "Current signals look steady. Maintain sleep consistency, hydration, planned study blocks, and short recovery breaks."

    chips = [
        ("Overall", overall),
        ("Balance", f"{balance_score}/100"),
        ("Stress load", f"{stress_score}/100"),
        ("Academic load", f"{academic_score}/100"),
    ]
    chip_html = "".join([f'<div class="review-chip"><span>{esc(label)}</span><strong>{esc(value)}</strong></div>' for label, value in chips])
    return f"""
<div class="premium-panel">
    <div class="panel-title-row">
        <strong>Clinical Review Snapshot</strong>
        <span class="badge {status_kind(overall)}">{esc(level)}</span>
    </div>
    <div class="recommendation-body">{esc(note)}</div>
    <div class="review-strip">{chip_html}</div>
</div>
"""


def domain_findings_html(a1, a2, a3):
    rows = [
        (
            "Physical",
            f"{clamp_score(a1.get('wellness_score'))}/100 - {a1.get('status', 'Pending')}",
            first_text(a1.get("immediate_actions")) or first_text(a1.get("observations")),
        ),
        (
            "Mental",
            f"{clamp_score(a2.get('stress_score'))}/100 - {a2.get('risk_level', 'Pending')}",
            first_text(a2.get("coping_recommendations")) or first_text(a2.get("observations")),
        ),
        (
            "Academic",
            f"{clamp_score(a3.get('academic_load_score'))}/100 - {a3.get('burnout_risk', 'Pending')}",
            first_text(a3.get("study_recommendations")) or first_text(a3.get("observations")),
        ),
    ]
    rows_html = "".join(
        [
            f"""
<div class="clinical-row">
    <div class="row-label">{esc(label)}</div>
    <div class="row-body"><strong>{esc(signal)}</strong><br>{esc(action)}</div>
</div>
"""
            for label, signal, action in rows
        ]
    )
    return f"""
<div class="premium-panel">
    <div class="panel-title-row">
        <strong>Domain Findings</strong>
        <span class="tiny">Signal and next step</span>
    </div>
    <div class="clinical-list">{rows_html}</div>
</div>
"""


def render_actions(actions):
    if not actions:
        st.info("No priority actions were returned yet.")
        return

    for index, action in enumerate(actions, 1):
        st.markdown(
            f"""
<div class="action-row">
    <div class="action-index">{index}</div>
    <div class="action-text">{esc(action)}</div>
</div>
""",
            unsafe_allow_html=True,
        )


def render_detail_block(title, observations, actions, action_title):
    with st.expander(title, expanded=False):
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**Observations**")
            for item in observations or []:
                st.write(f"- {item}")
        with col_b:
            st.markdown(f"**{action_title}**")
            for item in actions or []:
                st.write(f"- {item}")


def call_json(method, url, **kwargs):
    response = requests.request(method, url, **kwargs)
    if response.status_code >= 400:
        detail = response.text
        try:
            detail = response.json().get("detail", detail)
        except ValueError:
            pass
        raise RuntimeError(f"{response.status_code}: {detail}")
    return response.json()


def save_report(student_name, result):
    try:
        data = call_json(
            "POST",
            f"{API_URL}/save",
            json={"student_name": student_name, "results": result},
            timeout=30,
        )
        st.session_state.last_saved_id = data.get("report_id")
        return True
    except Exception as exc:
        st.warning(f"Report created, but saving failed: {exc}")
        return False


def prepare_pdf(student_name, result):
    if st.session_state.pdf_bytes is not None:
        return
    try:
        import pdf_generator

        pdf_generator = importlib.reload(pdf_generator)

        buffer = pdf_generator.generate_pdf(student_name, result)
        st.session_state.pdf_bytes = buffer.read()
        st.session_state.pdf_error = None
    except Exception as exc:
        st.session_state.pdf_bytes = None
        st.session_state.pdf_error = str(exc)


def render_report_actions(student_name, result):
    left, center, right = st.columns([1, 1.5, 1])
    with center:
        if st.session_state.isPdfReady and st.session_state.pdf_bytes:
            st.success("PDF ready. Download it from the sidebar.")
            return

        if st.button("Get PDF", type="primary", use_container_width=True, key="get_pdf_button"):
            st.session_state.pdf_bytes = None
            st.session_state.pdf_error = None
            with st.spinner("Preparing wellness PDF..."):
                prepare_pdf(student_name, result)
            st.session_state.isPdfReady = st.session_state.pdf_bytes is not None
            if st.session_state.isPdfReady:
                st.rerun()

        if st.session_state.isPdfReady and st.session_state.pdf_bytes:
            st.success("PDF ready. Download it from the sidebar.")
        elif st.session_state.pdf_error:
            st.warning(f"PDF could not be prepared: {st.session_state.pdf_error}")


def result_parts(result):
    return (
        result.get("agent1", {}),
        result.get("agent2", {}),
        result.get("agent3", {}),
        result.get("agent4", {}),
        result.get("agent5", {}),
    )


def result_used_fallback(result):
    return any((part or {}).get("_fallback") for part in result_parts(result))


def render_report(result, student_name):
    a1, a2, a3, a4, a5 = result_parts(result)

    section("Wellness Report")
    c1, c2, c3 = st.columns(3)
    with c1:
        score_card(
            "Physical Wellness",
            a1.get("wellness_score", 0),
            a1.get("status", "Pending"),
            first_text(a1.get("observations")),
        )
    with c2:
        score_card(
            "Mental Stress",
            a2.get("stress_score", 0),
            a2.get("risk_level", "Pending"),
            first_text(a2.get("observations")),
        )
    with c3:
        score_card(
            "Academic Load",
            a3.get("academic_load_score", 0),
            a3.get("burnout_risk", "Pending"),
            first_text(a3.get("observations")),
        )

    overall = a5.get("overall_status", "Pending")
    st.markdown(
        f"""
<div class="recommendation">
    <div class="recommendation-title">Recommendation - {esc(overall)}</div>
    <div class="recommendation-body">{esc(a5.get("summary", "No recommendation returned yet."))}</div>
</div>
""",
        unsafe_allow_html=True,
    )

    if a5.get("escalation_recommended"):
        st.error(f"Support recommended: {a5.get('escalation_reason', 'Review needed.')}")

    section("Priority Actions")
    render_actions(a5.get("priority_actions", []))

    section("Full Analysis")
    render_detail_block(
        "Physical wellness details",
        a1.get("observations", []),
        a1.get("immediate_actions", []),
        "Suggested actions",
    )
    render_detail_block(
        "Mental wellness details",
        a2.get("observations", []),
        a2.get("coping_recommendations", []),
        "Coping recommendations",
    )
    render_detail_block(
        "Academic load details",
        a3.get("observations", []),
        a3.get("study_recommendations", []),
        "Study recommendations",
    )

    if a4:
        with st.expander("Evidence note", expanded=False):
            takeaway = a4.get("key_takeaway")
            if takeaway:
                st.write(takeaway)
            for item in a4.get("relevant_evidence", []) or []:
                st.write(f"- {item}")

    section("Report Actions")
    render_report_actions(student_name, result)


def load_history(student_name):
    return call_json("GET", f"{API_URL}/history/{student_name}", timeout=15)


def average(reports, field, key):
    values = [safe_number((report.get(field) or {}).get(key)) for report in reports]
    return round(sum(values) / len(values)) if values else 0


def classify_activity(text):
    item = str(text or "").lower()
    if any(word in item for word in ["sleep", "rest", "nap"]):
        return "sleep"
    if any(word in item for word in ["study", "review", "class", "assignment", "exam", "pomodoro"]):
        return "study"
    if any(word in item for word in ["meal", "breakfast", "lunch", "dinner", "snack", "eat"]):
        return "food"
    if any(word in item for word in ["walk", "exercise", "yoga", "stretch", "workout", "gym"]):
        return "move"
    if any(word in item for word in ["meditat", "relax", "breath", "journ", "calm"]):
        return "calm"
    return "free"


def activity_icon(kind):
    return {
        "sleep": "SL",
        "study": "ST",
        "food": "ME",
        "move": "MV",
        "calm": "CA",
        "free": "FL",
    }.get(kind, "FL")


def activity_label(kind):
    return {
        "sleep": "Sleep",
        "study": "Study",
        "food": "Meals",
        "move": "Movement",
        "calm": "Calm",
        "free": "Flex",
    }.get(kind, "Flex")


def normalize_day_items(day_plan):
    if isinstance(day_plan, dict):
        return list(day_plan.items())
    if isinstance(day_plan, list):
        return [(f"Block {idx + 1}", activity) for idx, activity in enumerate(day_plan)]
    return []


def weekly_plan_summary_html(plan):
    schedule = plan.get("schedule", {}) or {}
    counts = {"sleep": 0, "study": 0, "food": 0, "move": 0, "calm": 0, "free": 0}
    total_blocks = 0
    earliest = ""
    latest = ""

    for day_plan in schedule.values():
        for time_label, activity in normalize_day_items(day_plan):
            kind = classify_activity(activity)
            counts[kind] = counts.get(kind, 0) + 1
            total_blocks += 1
            text_time = str(time_label)
            if not earliest:
                earliest = text_time.split("-")[0].strip()
            latest = text_time.split("-")[-1].strip()

    legend = "".join(
        [
            f'<span class="legend-pill"><b>{activity_icon(kind)}</b>{activity_label(kind)}</span>'
            for kind in ["sleep", "study", "food", "move", "calm", "free"]
        ]
    )
    routines = [
        ("Blocks", f"{total_blocks} planned"),
        ("Study", f"{counts.get('study', 0)} focused slots"),
        ("Recovery", f"{counts.get('calm', 0) + counts.get('move', 0)} reset slots"),
        ("Day span", f"{earliest or 'Start'} to {latest or 'End'}"),
    ]
    routine_html = "".join(
        [f'<div class="routine-row"><span>{esc(label)}</span><strong>{esc(value)}</strong></div>' for label, value in routines]
    )
    focus = plan.get("weekly_focus", "Keep sleep, study, movement, meals, and calm breaks consistent.")
    habits = plan.get("key_habits", []) or []
    habits_text = " · ".join([str(habit) for habit in habits[:3]]) or "Repeat the plan gently and adjust based on energy."
    return f"""
<div class="plan-dashboard">
    <div class="premium-panel">
        <div class="panel-title-row">
            <strong>Weekly Routine Map</strong>
            <span class="tiny">Followable at a glance</span>
        </div>
        <div class="recommendation-body">{esc(focus)}</div>
        <div class="plan-legend">{legend}</div>
    </div>
    <div class="premium-panel">
        <div class="panel-title-row">
            <strong>Routine Quality</strong>
            <span class="tiny">{len(schedule)} days</span>
        </div>
        <div class="routine-list">{routine_html}</div>
        <div class="tiny" style="margin-top:.75rem;">{esc(habits_text)}</div>
    </div>
</div>
"""


def render_plan_table(schedule):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    if not any(schedule.get(day) for day in days):
        st.info("The weekly plan did not return day-wise activities.")
        return

    cards = []
    for day in days:
        day_plan = schedule.get(day) or {}
        items = normalize_day_items(day_plan)

        if not items:
            item_html = """
<div class="plan-track">
    <div class="plan-item free">
        <span class="plan-icon">FL</span>
        <div class="plan-copy"><span class="time">Open</span><div class="plan-title">Recovery / flexible time</div></div>
    </div>
</div>
"""
        else:
            chunks = []
            for time_label, activity in items:
                kind = classify_activity(activity)
                chunks.append(
                    f"""
<div class="plan-item {kind}">
    <span class="plan-icon">{activity_icon(kind)}</span>
    <div class="plan-copy">
        <span class="time">{esc(time_label)}</span>
        <div class="plan-title">{esc(activity)}</div>
    </div>
</div>
"""
                )
            item_html = f'<div class="plan-track">{"".join(chunks)}</div>'

        cards.append(
            f"""
<div class="day-card">
    <div class="day-head">
        <div>
            <div class="day-name">{esc(day)}</div>
            <div class="day-sub">{esc("Recovery led" if day in {"Saturday", "Sunday"} else "Structured day")}</div>
        </div>
        <div class="day-count">{len(items)} blocks</div>
    </div>
    {item_html}
</div>
"""
        )

    st.markdown(
        f'<div class="weekly-grid">{"".join(cards)}</div>',
        unsafe_allow_html=True,
    )


def render_dashboard_page():
    if not st.session_state.result:
        render_header("Health Dashboard", "A calm overview of the latest wellness report and weekly routine.")
        st.info("Generate a Daily Check-In first. The dashboard will unlock after your latest report is ready.")
        return

    result = st.session_state.result
    a1, a2, a3, _a4, a5 = result_parts(result)
    student_name = st.session_state.currentStudent or st.session_state.result_name or "Student"

    overall = a5.get("overall_status", "Pending")
    physical_score = clamp_score(a1.get("wellness_score"))
    stress_score = clamp_score(a2.get("stress_score"))
    academic_score = clamp_score(a3.get("academic_load_score"))
    balance_score = round((physical_score + (100 - stress_score) + (100 - academic_score)) / 3)

    st.markdown(
        f"""
<div class="dashboard-hero">
    <div class="wellness-welcome">
        <div class="welcome-eyebrow">Wellness Dashboard</div>
        <div class="welcome-title">Welcome in, {esc(student_name)}</div>
        <div class="welcome-copy">{esc(a5.get("summary", "Your latest wellness report is ready."))}</div>
        <div class="wellness-pills">
            <span class="wellness-pill">{esc(overall)}</span>
            <span class="wellness-pill">Balance {balance_score}/100</span>
            <span class="wellness-pill">{datetime.now().strftime("%d %b")}</span>
        </div>
    </div>
    {calendar_strip_html()}
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
<div class="activity-grid">
    {activity_card_html("Physical Wellness", f"{physical_score}/100", a1.get("status", "Latest score"), "PW", "activity-blue")}
    {activity_card_html("Mental Stress", f"{stress_score}/100", a2.get("risk_level", "Latest score"), "MS", "activity-green")}
    {activity_card_html("Academic Load", f"{academic_score}/100", a3.get("burnout_risk", "Latest score"), "AL", "activity-violet")}
    {activity_card_html("Overall Balance", f"{balance_score}/100", overall, "OB", "activity-indigo")}
</div>
""",
        unsafe_allow_html=True,
    )

    overview_tab, plan_tab = st.tabs(["Overview", "Weekly Plan"])

    with overview_tab:
        left, right = st.columns([1.05, .95])
        with left:
            st.markdown(
                f"""
<div class="premium-panel">
    <div class="panel-title-row">
        <strong>Wellness Balance</strong>
        <span class="badge {status_kind(overall)}">{esc(overall)}</span>
    </div>
    {score_bar_html("Physical", physical_score)}
    {score_bar_html("Mental calm", 100 - stress_score)}
    {score_bar_html("Academic space", 100 - academic_score)}
    {chart_svg_html(physical_score, stress_score, academic_score, balance_score)}
</div>
""",
                unsafe_allow_html=True,
            )

            st.markdown(
                risk_interpretation(overall, physical_score, stress_score, academic_score, balance_score),
                unsafe_allow_html=True,
            )

        with right:
            st.markdown(domain_findings_html(a1, a2, a3), unsafe_allow_html=True)
            st.markdown(
                f"""
<div class="recommendation">
    <div class="recommendation-title">Care Summary - {esc(student_name)}</div>
    <div class="recommendation-body">{esc(a5.get("summary", "No recommendation returned yet."))}</div>
</div>
""",
                unsafe_allow_html=True,
            )
            section("Care Priorities")
            render_actions(a5.get("priority_actions", []))

    with plan_tab:
        st.markdown(
            """
<div class="panel-title-row">
    <strong>Weekly Planner</strong>
    <span class="tiny">Generated from latest report</span>
</div>
""",
            unsafe_allow_html=True,
        )
        if st.button("Generate Weekly Plan", type="primary", use_container_width=False):
            try:
                from weekly_plan import generate_weekly_plan

                with st.spinner("Building a balanced weekly plan..."):
                    st.session_state.weekly_plan = generate_weekly_plan(student_name, result)
                st.success("Weekly plan is ready.")
            except Exception as exc:
                st.error(f"Could not generate weekly plan: {exc}")

        plan = st.session_state.weekly_plan
        if not plan:
            st.info("Generate a weekly plan to see a modern day-by-day wellness calendar.")
            return

        st.markdown(weekly_plan_summary_html(plan), unsafe_allow_html=True)

        render_plan_table(plan.get("schedule", {}))


def render_history_page():
    render_header("Report History", "Review saved reports, trends, and previous wellness states.")

    section("Find Student")
    with st.form("history_search"):
        col_a, col_b = st.columns([4, 1])
        with col_a:
            lookup = st.text_input(
                "Student name",
                value=st.session_state.student_name,
                placeholder="Enter the student name used during check-in",
            )
        with col_b:
            st.write("")
            searched = st.form_submit_button("Search", use_container_width=True)

    if not searched:
        st.info("Search by student name to load saved reports.")
        return

    if not lookup.strip():
        st.warning("Enter a student name first.")
        return

    try:
        data = load_history(lookup.strip())
    except requests.exceptions.ConnectionError:
        st.error("The API server is not reachable. Start it with: uvicorn api:app --reload")
        return
    except Exception as exc:
        st.error(f"Could not load history: {exc}")
        return

    reports = data.get("reports", [])
    if not reports:
        st.info("No reports found for this name yet.")
        return

    chronological = list(reversed(reports))
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Reports", len(reports))
    c2.metric("Avg Physical", f"{average(reports, 'physical_wellness', 'wellness_score')}/100")
    c3.metric("Avg Stress", f"{average(reports, 'mental_stress', 'stress_score')}/100")
    c4.metric("Avg Academic", f"{average(reports, 'academic_load', 'academic_load_score')}/100")

    section("Score Trend")
    chart_data = pd.DataFrame(
        {
            "Physical": [
                safe_number((report.get("physical_wellness") or {}).get("wellness_score"))
                for report in chronological
            ],
            "Stress": [
                safe_number((report.get("mental_stress") or {}).get("stress_score"))
                for report in chronological
            ],
            "Academic": [
                safe_number((report.get("academic_load") or {}).get("academic_load_score"))
                for report in chronological
            ],
        }
    )
    st.line_chart(chart_data, height=260)

    section("Saved Reports")
    for report in reports:
        physical = report.get("physical_wellness") or {}
        mental = report.get("mental_stress") or {}
        academic = report.get("academic_load") or {}
        rec = report.get("recommendation") or {}
        timestamp = report.get("timestamp", "Unknown time")

        st.markdown(
            f"""
<div class="history-item">
    <div class="tiny">{esc(timestamp)}</div>
    <strong>{esc(rec.get("overall_status", "Report"))}</strong>
    <div class="tiny">
        Physical {safe_number(physical.get("wellness_score"))}/100 |
        Stress {safe_number(mental.get("stress_score"))}/100 |
        Academic {safe_number(academic.get("academic_load_score"))}/100
    </div>
</div>
""",
            unsafe_allow_html=True,
        )


def render_daily_page():
    render_header("Daily Check-In", "Enter today's wellness data and generate a clear report.")

    section("Student Profile")
    name = st.text_input(
        "Student name",
        value=st.session_state.student_name,
        placeholder="Enter your name",
        key="daily_student_name",
    )
    st.session_state.student_name = name

    section("Today Data")
    with st.form("checkin_form"):
        col_1, col_2, col_3 = st.columns(3)
        with col_1:
            st.markdown("**Physical**")
            sleep = st.slider("Sleep hours", 0.0, 12.0, 7.0, 0.5)
            water = st.slider("Water glasses", 0, 15, 6)
            exercise = st.slider("Exercise minutes", 0, 180, 20, 5)
            meals = st.slider("Meals today", 0, 6, 3)

        with col_2:
            st.markdown("**Mental**")
            stress = st.slider("Stress level", 1, 10, 5)
            mood = st.selectbox("Current mood", ["Calm", "Motivated", "Anxious", "Low", "Irritable"])
            stress_cause = st.text_input("Main stress cause", placeholder="Exams, deadline, personal issue")

        with col_3:
            st.markdown("**Academic**")
            study = st.slider("Study hours", 0.0, 16.0, 3.0, 0.5)
            deadlines = st.slider("Pending deadlines", 0, 20, 1)
            workload = st.slider("Workload pressure", 1, 10, 5)
            backlog = st.slider("Backlog subjects", 0, 10, 0)

        submitted = st.form_submit_button("Generate Wellness Report", type="primary", use_container_width=True)

    if submitted:
        if not name.strip():
            st.warning("Enter the student name before generating the report.")
        else:
            payload = {
                "student_name": name.strip(),
                "sleep_hours": sleep,
                "water_glasses": water,
                "exercise_minutes": exercise,
                "meals_today": meals,
                "stress_level": stress,
                "mood": mood,
                "stress_cause": stress_cause.strip() or "Not specified",
                "study_hours": study,
                "pending_deadlines": deadlines,
                "workload_rating": workload,
                "backlog_subjects": backlog,
            }

            # --- Progress UI with background thread ---
            step_labels = [
                "Physical wellness",
                "Mental stress",
                "Academic load",
                "Evidence base search",
                "Final recommendation",
            ]
            # Time estimates per step (seconds) — generous to handle retries
            # agents 1-3 run in parallel (~20s with retries), agent 4 (~15s), agent 5 (~15s)
            step_durations = [5, 5, 5, 4, 6]

            progress_placeholder = st.empty()

            def render_progress(done_steps, running_label, pct):
                steps_html = ""
                for label in done_steps:
                    steps_html += f'<div class="progress-step done"><span class="step-icon">✓</span> {esc(label)}</div>'
                if running_label:
                    steps_html += f'<div class="progress-step running"><span class="step-icon">⟳</span> {esc(running_label)}</div>'
                remaining = [s for s in step_labels if s not in done_steps and s != running_label]
                for label in remaining:
                    steps_html += f'<div class="progress-step pending"><span class="step-icon">○</span> {esc(label)}</div>'
                progress_placeholder.markdown(
                    f"""
<div class="progress-container">
    <div class="progress-title">Generating Wellness Report</div>
    <div class="progress-percent">{pct}%</div>
    <div class="progress-bar-track"><div class="progress-bar-fill" style="width:{pct}%"></div></div>
    <div class="progress-steps">{steps_html}</div>
</div>
""",
                    unsafe_allow_html=True,
                )

            # Run the API call in a background thread
            result_holder = {"result": None, "error": None, "done": False}

            def api_call():
                try:
                    result_holder["result"] = call_json(
                        "POST", f"{API_URL}/analyze", json=payload, timeout=75
                    )
                except Exception as e:
                    result_holder["error"] = e
                result_holder["done"] = True

            thread = threading.Thread(target=api_call, daemon=True)
            thread.start()

            # Maximum wait time: 5 minutes (the backend itself will time out or error)
            max_wait = 80
            elapsed = 0.0
            poll_interval = 0.5
            total_time = sum(step_durations)
            tick = 0

            while not result_holder["done"]:
                if elapsed >= max_wait:
                    result_holder["error"] = RuntimeError("Request timed out after 80 seconds. The LLM service may be overloaded; please try again.")
                    result_holder["done"] = True
                    break

                # Calculate which step we're on based on elapsed time
                cumulative = 0
                current_step_idx = 0
                for i, duration in enumerate(step_durations):
                    cumulative += duration
                    if elapsed < cumulative:
                        current_step_idx = i
                        break
                else:
                    current_step_idx = len(step_labels) - 1

                done_steps = step_labels[:current_step_idx]

                if elapsed >= total_time:
                    # Past our estimate — show all steps done, with a finishing message
                    done_steps = step_labels[:-1]
                    running_label = "Finishing up..."
                    # Slowly creep from 93% to 98% instead of oscillating
                    overtime = elapsed - total_time
                    pct = min(98, 93 + int(overtime / 12))
                else:
                    running_label = step_labels[current_step_idx] + "..."
                    pct = min(91, int((elapsed / total_time) * 100))

                render_progress(done_steps, running_label, pct)
                _time.sleep(poll_interval)
                elapsed += poll_interval
                tick += 1

            # Thread finished — show final state
            if result_holder["result"]:
                render_progress(step_labels, "", 100)
                _time.sleep(0.4)
                progress_placeholder.empty()

                result = result_holder["result"]
                
                # Check if provider was auto-switched
                provider_switched = result.pop("_provider_switched", False)
                provider_name = result.pop("_provider", "gemini")
                switch_reason = result.pop("_provider_switch_reason", "")

                st.session_state.currentStudent = name.strip()
                st.session_state.student_name = name.strip()
                st.session_state.result = result
                st.session_state.result_name = name.strip()
                st.session_state.pdf_bytes = None
                st.session_state.pdf_error = None
                st.session_state.isPdfReady = False
                st.session_state.weekly_plan = None
                st.session_state.last_saved_id = None
                saved = save_report(name.strip(), result)
                if saved:
                    st.success("Report generated and saved.")
                else:
                    st.success("Report generated.")

                if result_used_fallback(result):
                    st.info("AI provider was unavailable, so WellMind used its built-in analysis rules to finish the report quickly.")

                # Show provider switch notification
                if provider_switched:
                    provider_display = "Groq (Llama 3.3)" if provider_name == "groq" else "Gemini"
                    st.markdown(
                        f"""
<div class="provider-toast">
    <div class="toast-icon">⚡</div>
    <div>
        <div class="toast-text">Switched to {esc(provider_display)}</div>
        <div class="toast-sub">{esc(switch_reason)}</div>
    </div>
</div>
""",
                        unsafe_allow_html=True,
                    )

            elif result_holder["error"]:
                progress_placeholder.empty()
                error_str = str(result_holder["error"])
                error_lower = error_str.lower()
                retryable_keywords = ["429", "resource_exhausted", "quota", "503", "unavailable", "high demand", "overloaded", "rate limit", "timed out"]
                if any(kw in error_lower for kw in retryable_keywords):
                    st.markdown(
                        """
<div class="quota-card">
    <div class="quota-title">⚠ LLM Service Temporarily Unavailable</div>
    <div class="quota-body">
        The AI model is currently experiencing high demand or rate limits.
        This usually resolves within 1–2 minutes. Please wait briefly and try again.
    </div>
</div>
""",
                        unsafe_allow_html=True,
                    )
                elif "Connection" in error_str or "ConnectionError" in error_str:
                    st.error("The API server is not reachable. Start it with: uvicorn api:app --reload")
                else:
                    st.error(f"Analysis failed: {error_str}")

    if st.session_state.result:
        render_report(st.session_state.result, st.session_state.result_name or name)
    else:
        st.info("Fill the form and generate a wellness report. Results and PDF download will appear here.")


with st.sidebar:
    st.markdown(
        """
<div class="wm-brand">
    <span class="wm-mark">WM</span>
    <span class="wm-brand-title">WellMind AI<span class="wm-brand-sub">Student Wellness</span></span>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sidebar-section-title">Navigation</div>', unsafe_allow_html=True)
    selected = st.radio(
        "Navigation",
        PAGES,
        index=PAGES.index(st.session_state.page) if st.session_state.page in PAGES else 0,
        label_visibility="collapsed",
    )
    st.session_state.page = selected

    st.divider()
    st.markdown('<div class="sidebar-section-title">Student</div>', unsafe_allow_html=True)
    active_student = st.session_state.currentStudent or "No active student"
    st.markdown(
        f"""
<div class="sidebar-bottom-panel">
    <div class="tiny">Active Student</div>
    <div class="sidebar-student">{esc(active_student)}</div>
</div>
""",
        unsafe_allow_html=True,
    )

    if st.session_state.result:
        status = (st.session_state.result.get("agent5") or {}).get("overall_status", "Report ready")
        st.markdown(
            f'<span class="badge {status_kind(status)}">{esc(status)}</span>',
            unsafe_allow_html=True,
        )

        st.markdown('<div class="sidebar-section-title">Report PDF</div>', unsafe_allow_html=True)
        if st.session_state.isPdfReady and st.session_state.pdf_bytes:
            _pdf_name = (st.session_state.currentStudent or st.session_state.result_name or "student").strip().replace(" ", "_")
            st.download_button(
                "Download PDF",
                data=st.session_state.pdf_bytes,
                file_name=f"WellMind_{_pdf_name}.pdf",
                mime="application/pdf",
                use_container_width=True,
                key="sidebar_pdf_download",
            )
        elif st.session_state.pdf_error:
            st.caption("PDF could not be prepared. Use Get PDF again.")
        else:
            st.caption("Click Get PDF at the end of the report.")
    else:
        st.caption("No report generated in this session yet.")


if st.session_state.page == "Daily Check-In":
    render_daily_page()
elif st.session_state.page == "History":
    render_history_page()
else:
    render_dashboard_page()
