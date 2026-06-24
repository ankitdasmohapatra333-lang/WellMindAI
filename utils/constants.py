"""WellMind AI - Constants"""

# Color Palette
COLORS = {
    "background": "#07131F",
    "surface": "#0F1D2D",
    "surface2": "#152436",
    "primary": "#00E5B0",
    "secondary": "#5EEAD4",
    "purple": "#8B5CF6",
    "pink": "#EC4899",
    "orange": "#F59E0B",
    "text": "#FFFFFF",
    "text_secondary": "#94A3B8",
    "border": "rgba(0, 229, 176, 0.15)",
    "card": "rgba(15, 29, 45, 0.8)",
}

# Agent names
AGENTS = [
    {"name": "Physical Wellness Agent", "icon": "🫀", "desc": "Analyzing sleep, hydration & exercise patterns"},
    {"name": "Mental Stress Agent", "icon": "🧠", "desc": "Evaluating stress levels & mental load"},
    {"name": "Academic Load Agent", "icon": "📚", "desc": "Assessing study hours & cognitive demand"},
    {"name": "RAG Knowledge Agent", "icon": "🔍", "desc": "Retrieving evidence-based wellness research"},
    {"name": "Recommendation Agent", "icon": "✨", "desc": "Generating personalized wellness plan"},
]

# Grade thresholds
GRADE_MAP = {
    (90, 100): ("A+", "#00E5B0"),
    (80, 90): ("A", "#00E5B0"),
    (70, 80): ("B", "#5EEAD4"),
    (60, 70): ("C", "#F59E0B"),
    (50, 60): ("D", "#F97316"),
    (0, 50): ("F", "#EF4444"),
}

# Navigation
NAV_ITEMS = ["Home", "Assessment", "Analysis", "Results", "History"]
NAV_ICONS = ["house", "clipboard-check", "cpu", "bar-chart-line", "clock-history"]

API_BASE = "http://localhost:8000"
