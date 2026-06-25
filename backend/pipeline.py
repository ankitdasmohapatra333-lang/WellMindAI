# ============================================
# WELLMIND AI — Pipeline (The Engine)
# ============================================
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'agents')))

from agent1 import analyze_physical_wellness
from agent2 import analyze_mental_stress
from agent3 import analyze_academic_load
from agent4 import rag_knowledge_agent
from agent5 import generate_recommendation
from database import save_report


def run_full_pipeline(student_name, sleep_hours, water_glasses, exercise_minutes, meals_today,
                       stress_level, mood, stress_cause,
                       study_hours, pending_deadlines, workload_rating, backlog_subjects,
                       auto_save=True):
    
    agent1_result = analyze_physical_wellness(sleep_hours, water_glasses, exercise_minutes, meals_today)
    agent2_result = analyze_mental_stress(stress_level, mood, stress_cause)
    agent3_result = analyze_academic_load(study_hours, pending_deadlines, workload_rating, backlog_subjects)
    
    rag_query = f"Sleep status: {agent1_result['status']}, Stress risk: {agent2_result['risk_level']}, Academic burnout risk: {agent3_result['burnout_risk']}"
    agent4_result = rag_knowledge_agent(rag_query)
    
    agent5_result = generate_recommendation(agent1_result, agent2_result, agent3_result, agent4_result)
    
    full_results = {
        "agent1": agent1_result,
        "agent2": agent2_result,
        "agent3": agent3_result,
        "agent4": agent4_result,
        "agent5": agent5_result,
    }
    
    if auto_save:
        report_id = save_report(student_name, full_results)
        full_results["report_id"] = report_id
    
    return full_results


if __name__ == "__main__":
    print("=" * 50)
    print("WellMind AI — FULL PIPELINE TEST")
    print("=" * 50)
    
    result = run_full_pipeline(
        student_name="Test Student",
        sleep_hours=5, water_glasses=3, exercise_minutes=0, meals_today=2,
        stress_level=8, mood="Anxious", stress_cause="Upcoming exams",
        study_hours=2, pending_deadlines=3, workload_rating=9, backlog_subjects=2
    )
    
    print(f"Report ID: {result['report_id']}")
    print(f"Overall Status: {result['agent5']['overall_status']}")
    print("Full pipeline working end-to-end.")