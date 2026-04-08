import sys
import os

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.environment import MedicalEnv


def simple_rule_based_model(state):
    symptoms = [s.lower() for s in state["symptoms"]]

    if "fever" in symptoms and "cough" in symptoms:
        return {
            "disease": "flu",
            "severity": "mild",
            "treatment": "rest and fluids",
            "reason": "fever and cough indicate flu"
        }

    elif "chest pain" in symptoms:
        return {
            "disease": "angina",
            "severity": "moderate",
            "treatment": "medication and rest",
            "reason": "chest pain is a key symptom"
        }

    elif "itching" in symptoms or "rash" in symptoms:
        return {
            "disease": "allergy",
            "severity": "mild",
            "treatment": "antihistamines",
            "reason": "skin irritation suggests allergy"
        }

    else:
        return {
            "disease": "unknown",
            "severity": "uncertain",
            "treatment": "consult doctor",
            "reason": "insufficient symptoms"
        }


def run_simulation():
    print("HELLO RUNNING")

    env = MedicalEnv()

    total_score = 0
    num_cases = 5

    for i in range(num_cases):
        print(f"\n=== CASE {i+1} ===")

        state = env.reset()
        print("PATIENT DATA:", state)

        # Normalize data
        symptoms = [s.lower() for s in state["symptoms"]]
        symptoms_set = set(symptoms)
        history = [h.lower() for h in state["history"]]

        # AI LOGIC (HARD → EASY)

        if {"severe headache", "blurred vision"}.issubset(symptoms_set) and "high blood pressure" in history:
            disease = "stroke"
            treatment = "immediate hospitalization"
            severity = "severe"

        elif {"chest pain", "sweating", "nausea"}.issubset(symptoms_set):
            disease = "heart attack"
            treatment = "immediate hospitalization"
            severity = "severe"

        elif {"shortness of breath", "fatigue"}.issubset(symptoms_set) and "high blood pressure" in history:
            disease = "heart failure"
            treatment = "urgent medical care"
            severity = "severe"

        elif {"confusion", "memory loss"}.issubset(symptoms_set):
            disease = "alzheimer's"
            treatment = "supportive care"
            severity = "severe"

        elif {"frequent urination", "increased thirst"}.issubset(symptoms_set):
            disease = "diabetes"
            treatment = "diet control and medication"
            severity = "moderate"

        elif {"fever", "body pain", "headache"}.issubset(symptoms_set):
            disease = "dengue"
            treatment = "hydration and monitoring"
            severity = "moderate"

        elif {"abdominal pain", "vomiting"}.issubset(symptoms_set):
            disease = "food poisoning"
            treatment = "hydration and rest"
            severity = "moderate"

        elif {"itching", "rash"}.issubset(symptoms_set):
            disease = "allergy"
            treatment = "antihistamines"
            severity = "mild"

        elif {"sneezing", "runny nose"}.issubset(symptoms_set):
            disease = "common cold"
            treatment = "antihistamines"
            severity = "mild"

        elif {"sore throat", "fever"}.issubset(symptoms_set):
            disease = "throat infection"
            treatment = "warm fluids and rest"
            severity = "mild"

        elif len(symptoms) <= 1:
            disease = "unknown"
            treatment = "need more information"
            severity = "uncertain"

        elif "fever" in symptoms:
            disease = "flu"
            treatment = "rest and fluids"
            severity = "mild"

        elif "headache" in symptoms or "sensitivity to light" in symptoms:
            disease = "migraine"
            treatment = "pain relievers"
            severity = "mild"

        elif "chest pain" in symptoms:
            disease = "angina"
            treatment = "medication and rest"
            severity = "moderate"

        else:
            disease = "unknown"
            treatment = "consult doctor"
            severity = "uncertain"

        reason_text = f"Symptoms include {', '.join(symptoms)} suggesting {disease}"

        action = {
            "disease": disease,
            "severity": severity,
            "treatment": treatment,
            "reason": reason_text
        }

        result = env.step(action)

        print("RESULT:", result)
        total_score += result["reward"]

    average_score = total_score / num_cases

    print("\n=== FINAL PERFORMANCE ===")
    print("Average Score:", average_score)
    print("\nExecution completed successfully.")

    # OPTIONAL USER INPUT (safe for HF) true
    try:
        choice = input("\nDo you want to test custom input? (yes/no): ")

        if choice.lower() == "yes":
            age = int(input("Enter age: "))
            symptoms = input("Enter symptoms (comma separated): ").split(",")

            state = {
                "age": age,
                "symptoms": [s.strip().lower() for s in symptoms],
                "history": []
            }

            action = simple_rule_based_model(state)

            print("\n=== CUSTOM PREDICTION ===")
            print("Input:", state)
            print("Prediction:", action)

    except:
        print("\nCustom input skipped (non-interactive mode).")


# ✅ CRITICAL: prevents double execution
if __name__ == "__main__":
    run_simulation()
