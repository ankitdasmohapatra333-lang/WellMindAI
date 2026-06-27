import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'agents')))
from utils import ask_gemini

def _fallback_weekly_plan(student_name, analysis, reason=""):
    a1 = analysis.get("agent1", {})
    a2 = analysis.get("agent2", {})
    a3 = analysis.get("agent3", {})
    stress_high = str(a2.get("risk_level", "")).lower() in {"high", "severe"} or a2.get("stress_score", 0) >= 65
    academic_high = str(a3.get("burnout_risk", "")).lower() in {"high", "severe"} or a3.get("academic_load_score", 0) >= 65
    physical_low = str(a1.get("status", "")).lower() in {"fair", "poor"} or a1.get("wellness_score", 100) < 65

    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    schedule = {}
    for day in weekdays:
        weekend = day in {"Saturday", "Sunday"}
        wake = "06:45-07:00" if weekend else "06:15-06:30"
        first_study = "Priority study block" if academic_high and not weekend else "Concept revision"
        second_study = "Backlog catch-up" if academic_high else "Assignment progress"
        evening_reset = "Breathing and journaling" if stress_high else "Calm screen-free break"
        movement = "Evening walk" if physical_low else "Outdoor movement"
        schedule[day] = {
            wake: "Wake and hydrate",
            "07:00-07:25": "Breakfast",
            "07:30-07:45": "Light stretch",
            "09:00-10:30": first_study if not weekend else "Light weekly review",
            "10:30-10:45": "Short reset break",
            "11:15-12:15": second_study if not weekend else "Hobby or recovery",
            "13:00-13:30": "Lunch",
            "15:30-16:00": "Snack and planning",
            "17:00-17:35": movement,
            "18:30-18:45": evening_reset,
            "20:00-20:30": "Plan tomorrow",
            "22:30-06:30": "Sleep",
        }

    plan = {
        "weekly_focus": f"{student_name}, keep the week steady with sleep, short recovery breaks, and focused study blocks.",
        "key_habits": [
            "Sleep and wake at consistent times",
            "Use Pomodoro blocks for priority work",
            "Take one daily movement reset",
        ],
        "schedule": schedule,
        "slot_types": {
            "sleep": "sleep",
            "study": "study",
            "revision": "study",
            "break": "calm",
            "breathing": "calm",
            "walk": "move",
            "movement": "move",
            "breakfast": "food",
            "lunch": "food",
        },
    }
    if reason:
        plan["_fallback"] = True
        plan["_fallback_reason"] = reason
    return plan


def generate_weekly_plan(student_name, analysis):
    a1 = analysis.get("agent1", {})
    a2 = analysis.get("agent2", {})
    a3 = analysis.get("agent3", {})
    a5 = analysis.get("agent5", {})

    prompt = f"""
    You are a student wellness advisor. Based on this student's wellness data,
    create a personalized 7-day healthy weekly timetable.

    Student: {student_name}
    Physical Wellness: {a1.get('wellness_score',0)}/100 — {a1.get('status','unknown')}
    Mental Stress: {a2.get('stress_score',0)}/100 — {a2.get('risk_level','unknown')}
    Academic Load: {a3.get('academic_load_score',0)}/100 — {a3.get('burnout_risk','unknown')}
    Overall Status: {a5.get('overall_status','unknown')}

    Rules for the schedule:
    - If stress is High or Severe, include at least 2 relaxation/meditation slots daily
    - If physical wellness is Poor, include morning and evening walk slots
    - If academic load is High, include structured study blocks with Pomodoro breaks
    - Keep sleep time realistic (10:30 PM to 6:30 AM minimum)
    - Include meals at fixed times for routine stability
    - Saturday/Sunday should be lighter on study, heavier on recovery

    Return ONLY valid JSON with exactly this structure:
    {{
        "weekly_focus": "one sentence describing this week's main goal",
        "key_habits": ["habit 1", "habit 2", "habit 3"],
        "schedule": {{
            "Monday":    {{"05:30-06:30": "activity", "06:30-07:00": "activity", ... (cover full day in slots)}},
            "Tuesday":   {{"05:30-06:30": "activity", ...}},
            "Wednesday": {{"05:30-06:30": "activity", ...}},
            "Thursday":  {{"05:30-06:30": "activity", ...}},
            "Friday":    {{"05:30-06:30": "activity", ...}},
            "Saturday":  {{"06:00-07:00": "activity", ...}},
            "Sunday":    {{"06:00-07:00": "activity", ...}}
        }},
        "slot_types": {{
            "activity name keywords": "type"
        }}
    }}

    Each day should have 8-10 time slots covering the full waking day.
    Keep activity names short (max 5 words).
    Return ONLY JSON, no explanation.
    """
    try:
        return ask_gemini(prompt)
    except Exception as exc:
        return _fallback_weekly_plan(student_name, analysis, str(exc)[:160])
