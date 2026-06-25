import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'agents')))
from utils import ask_gemini


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
    return ask_gemini(prompt)