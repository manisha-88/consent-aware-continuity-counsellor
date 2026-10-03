import csv
import json
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
SYNTHETIC_DIR = BASE_DIR / "data" / "synthetic"
TEST_CASES_DIR = BASE_DIR / "data" / "test_cases"

# Predefined diverse clinical templates
CATEGORIES = ["exam_stress", "academic_concern", "family_information", "sleep_difficulty", "social_support", "safety_concern"]
CONSENT_STATUSES = ["ALLOWED", "RESTRICTED", "UNKNOWN"]

SCENARIOS = [
    {"summary": "Student experiences extreme anxiety before final examinations and struggles with insomnia.", "risk": "LOW", "cats": ["exam_stress", "sleep_difficulty"]},
    {"summary": "Client reports severe tension with parents due to failing academic grades.", "risk": "LOW", "cats": ["family_information", "academic_concern"]},
    {"summary": "Client expresses feeling completely isolated in dorms and unable to establish social support.", "risk": "LOW", "cats": ["social_support"]},
    {"summary": "Student states 'I do not know how much longer I can continue like this' after failing midterm.", "risk": "AMBIGUOUS", "cats": ["academic_concern"]},
    {"summary": "Client reports feeling unsafe in current living environment due to immediate danger.", "risk": "URGENT", "cats": ["safety_concern"]},
    {"summary": "Student mentions severe sleep loss due to upcoming thesis submission and family pressure.", "risk": "LOW", "cats": ["sleep_difficulty", "family_information", "exam_stress"]},
    {"summary": "Client feels overwhelmed by coursework and admits thinking about giving up completely.", "risk": "AMBIGUOUS", "cats": ["academic_concern"]},
    {"summary": "Student reports feeling lonely and isolated while struggling with grade drop.", "risk": "LOW", "cats": ["social_support", "academic_concern"]},
]

GOAL_TEMPLATES = [
    "Develop healthy coping mechanisms for stress.",
    "Improve sleep hygiene and evening routines.",
    "Establish active social support networks on campus.",
    "Set boundaries with family members regarding academic pressure.",
    "Create a realistic study timetable for exams.",
]

ACTION_TEMPLATES = [
    "Schedule follow-up counseling session in 2 weeks.",
    "Refer to campus academic support center.",
    "Complete daily sleep tracking journal.",
    "Provide contact info for student support groups.",
]

def generate_corpus(total_clients=30):
    SYNTHETIC_DIR.mkdir(parents=True, exist_ok=True)
    TEST_CASES_DIR.mkdir(parents=True, exist_ok=True)

    clients, sessions, consent_choices, goals, pending_actions, evaluation_cases = [], [], [], [], [], []

    for i in range(1, total_clients + 1):
        client_id = f"C{i:03d}"
        session_id = f"S{i:03d}"
        scenario = random.choice(SCENARIOS)

        # 1. Clients CSV
        clients.append({"client_id": client_id})

        # 2. Sessions CSV
        sessions.append({
            "session_id": session_id,
            "client_id": client_id,
            "session_date": f"2026-10-{(i % 28) + 1:02d}",
            "session_summary": scenario["summary"]
        })

        # 3. Consent Choices CSV
        client_categories = scenario["cats"]
        for cat in CATEGORIES:
            status = random.choice(CONSENT_STATUSES) if cat in client_categories else "UNKNOWN"
            consent_choices.append({
                "client_id": client_id,
                "category": cat,
                "status": status
            })

        # 4. Goals CSV
        goals.append({
            "client_id": client_id,
            "goal": random.choice(GOAL_TEMPLATES)
        })

        # 5. Pending Actions CSV
        pending_actions.append({
            "client_id": client_id,
            "action": random.choice(ACTION_TEMPLATES)
        })

        # 6. Evaluation Cases JSON
        evaluation_cases.append({
            "client_id": client_id,
            "expected_risk": scenario["risk"],
            "categories_present": scenario["cats"]
        })

    # Write CSVs
    write_csv(SYNTHETIC_DIR / "clients.csv", ["client_id", "name"], clients)
    write_csv(SYNTHETIC_DIR / "sessions.csv", ["session_id", "client_id", "session_date", "session_summary"], sessions)
    write_csv(SYNTHETIC_DIR / "consent_choices.csv", ["client_id", "category", "status"], consent_choices)
    write_csv(SYNTHETIC_DIR / "goals.csv", ["client_id", "goal"], goals)
    write_csv(SYNTHETIC_DIR / "pending_actions.csv", ["client_id", "action"], pending_actions)

    # Write Evaluation JSON
    with open(TEST_CASES_DIR / "evaluation_cases.json", "w", encoding="utf-8") as f:
        json.dump(evaluation_cases, f, indent=4)

    print(f" Successfully generated {total_clients} diverse clinical cases in {SYNTHETIC_DIR} and {TEST_CASES_DIR}")

def write_csv(filepath, fieldnames, rows):
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

if __name__ == "__main__":
    generate_corpus(30)