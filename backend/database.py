# ============================================
# WELLMIND AI — Database Layer
# ============================================

from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
mongo_uri = os.getenv("MONGO_URI")

client = MongoClient(mongo_uri)
db = client["wellmind_db"]
reports_collection = db["reports"]


def save_report(student_name, agent_results):
    report = {
        "student_name": student_name,
        "timestamp": datetime.now(),
        "physical_wellness": agent_results.get("agent1"),
        "mental_stress": agent_results.get("agent2"),
        "academic_load": agent_results.get("agent3"),
        "knowledge_evidence": agent_results.get("agent4"),
        "recommendation": agent_results.get("agent5"),
    }
    result = reports_collection.insert_one(report)
    return str(result.inserted_id)


def get_history(student_name):
    reports = reports_collection.find(
        {"student_name": student_name}
    ).sort("timestamp", -1)
    return list(reports)


if __name__ == "__main__":
    print("Testing MongoDB connection...")
    test_id = save_report("Test Student", {
        "agent1": {"wellness_score": 75, "status": "Good"},
        "agent2": {"stress_score": 40, "risk_level": "Low"},
    })
    print(f"Report saved with ID: {test_id}")
    history = get_history("Test Student")
    print(f"Found {len(history)} report(s) for Test Student")
    print("MongoDB connection working successfully.")