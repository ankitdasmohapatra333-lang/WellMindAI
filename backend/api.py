# ============================================
# WELLMIND AI — FastAPI Backend
# 3 routes wrapping pipeline.py + database.py
# + provider status endpoint for auto-switch UI
# ============================================

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'agents')))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pipeline import run_full_pipeline
from database import save_report, get_history
from utils import get_provider_state

app = FastAPI(title="WellMind AI Backend")

class StudentInput(BaseModel):
    student_name: str
    sleep_hours: float
    water_glasses: int
    exercise_minutes: int
    meals_today: int
    stress_level: int
    mood: str
    stress_cause: str
    study_hours: float
    pending_deadlines: int
    workload_rating: int
    backlog_subjects: int

class SaveInput(BaseModel):
    student_name: str
    results: dict

@app.post("/analyze")
def analyze(data: StudentInput):
    try:
        result = run_full_pipeline(
            student_name=data.student_name,
            sleep_hours=data.sleep_hours, water_glasses=data.water_glasses,
            exercise_minutes=data.exercise_minutes, meals_today=data.meals_today,
            stress_level=data.stress_level, mood=data.mood, stress_cause=data.stress_cause,
            study_hours=data.study_hours, pending_deadlines=data.pending_deadlines,
            workload_rating=data.workload_rating, backlog_subjects=data.backlog_subjects,
            auto_save=False
        )
        # Attach provider info to the result so the frontend can show a toast
        provider = get_provider_state()
        result["_provider"] = provider["current"]
        result["_provider_switched"] = provider["switched"]
        result["_provider_switch_reason"] = provider["switch_reason"]

        # Reset the switch flag after reading it
        provider["switched"] = False

        return result
    except Exception as e:
        error_msg = str(e).lower()
        retryable_keywords = ["429", "resource_exhausted", "quota", "503", "unavailable", "high demand", "overloaded", "rate limit"]
        if any(kw in error_msg for kw in retryable_keywords):
            raise HTTPException(status_code=429, detail="LLM service temporarily unavailable. Please wait a moment and try again.")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/save")
def save(data: SaveInput):
    try:
        report_id = save_report(data.student_name, data.results)
        return {"report_id": report_id}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Report generated, but database save failed: {str(e)}")

@app.get("/history/{student_name}")
def history(student_name: str):
    reports = get_history(student_name)
    for r in reports:
        r["_id"] = str(r["_id"])
        r["timestamp"] = str(r["timestamp"])
    return {"count": len(reports), "reports": reports}
