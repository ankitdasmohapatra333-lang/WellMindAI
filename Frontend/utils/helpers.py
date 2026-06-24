"""WellMind AI - Helper Functions"""
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from utils.constants import GRADE_MAP


def get_grade(score: float):
    for (low, high), (grade, color) in GRADE_MAP.items():
        if low <= score <= high:
            return grade, color
    return "F", "#EF4444"


def get_burnout_label(risk: float):
    if risk < 25:
        return "Low Risk", "#00E5B0"
    elif risk < 50:
        return "Moderate Risk", "#F59E0B"
    elif risk < 75:
        return "High Risk", "#F97316"
    return "Critical Risk", "#EF4444"


def get_stress_label(level: str):
    labels = {
        "Low": ("#00E5B0", 20),
        "Moderate": ("#F59E0B", 50),
        "High": ("#F97316", 75),
        "Severe": ("#EF4444", 90),
    }
    return labels.get(level, ("#00E5B0", 20))


def generate_mock_history():
    """Generate 7-day mock wellness history"""
    dates = [(datetime.now() - timedelta(days=i)).strftime("%b %d") for i in range(6, -1, -1)]
    np.random.seed(42)
    return pd.DataFrame({
        "Date": dates,
        "Wellness Score": np.random.randint(60, 90, 7).tolist(),
        "Sleep Hours": np.round(np.random.uniform(5.5, 8.5, 7), 1).tolist(),
        "Stress Level": np.random.randint(2, 8, 7).tolist(),
        "Burnout Risk": np.random.randint(20, 65, 7).tolist(),
        "Study Hours": np.random.randint(3, 9, 7).tolist(),
    })


def init_session_state():
    defaults = {
        "page": "Home",
        "assessment_data": None,
        "analysis_result": None,
        "history": generate_mock_history(),
        "agent_statuses": {},
        "analysis_complete": False,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val
