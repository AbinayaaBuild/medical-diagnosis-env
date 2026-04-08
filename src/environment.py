import json
import random
from pydantic import BaseModel
from typing import List


# ✅ Pydantic Models
class Observation(BaseModel):
    age: int
    symptoms: List[str]
    history: List[str]


class Action(BaseModel):
    disease: str
    severity: str
    treatment: str
    reason: str


class MedicalEnv:
    def __init__(self):
        with open("dataset/medical_cases.json", "r") as file:
            self.data = json.load(file)
        self.current_case = None

    def reset(self, difficulty=None):
        if difficulty:
            filtered = [case for case in self.data if case["difficulty"] == difficulty]
            self.current_case = random.choice(filtered)
        else:
            self.current_case = random.choice(self.data)

        return self.get_state()

    def get_state(self):
        return Observation(
            age=self.current_case["age"],
            symptoms=self.current_case["symptoms"],
            history=self.current_case["history"]
        ).dict()

    # ✅ OpenEnv required
    def state(self):
        return self.current_case

    def step(self, action):
        # ✅ Validate using Pydantic
        action = Action(**action)

        correct = self.current_case
        score = 0.0

        # ✅ 1. Disease check
        if action.disease.lower() == correct["disease"].lower():
            score += 0.4

        # ✅ 2. Severity check
        if action.severity.lower() == correct["severity"].lower():
            score += 0.2

        # ✅ 3. Treatment check
        if action.treatment:
            user_treat = action.treatment.lower()
            correct_treat = correct["treatment"].lower()

            if user_treat in correct_treat or correct_treat in user_treat:
                score += 0.2

        # ✅ 4. Reason check
        if action.reason:
            reason_text = action.reason.lower()
            match_count = sum(
                1 for symptom in correct["symptoms"] if symptom in reason_text
            )
            score += (match_count / len(correct["symptoms"])) * 0.2

        # ✅ FINAL RETURN (OpenEnv compliant)
        return {
            "observation": self.get_state(),
            "reward": round(score, 2),
            "done": True,
            "info": {"correct_answer": correct}
        }
