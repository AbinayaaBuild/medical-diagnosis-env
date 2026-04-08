import os
import json
from openai import OpenAI
from src.environment import MedicalEnv

# Load environment variables
API_BASE_URL = os.getenv("APIBASEURL")
MODEL_NAME = os.getenv("MODELNAME")
HF_TOKEN = os.getenv("HFTOKEN")  # keep this as is

# Initialize client ONLY if API key exists
client = None
if HF_TOKEN:
    client = OpenAI(
        base_url=API_BASE_URL,
        api_key=HF_TOKEN
    )

env = MedicalEnv()

print("[START]")

num_cases = 5
total_reward = 0

for i in range(num_cases):
    state = env.reset()

    print(f"[STEP] Case {i+1}")
    print(f"[STEP] Observation: {state}")

    prompt = f"""
You are a medical diagnosis AI.

Patient details:
Age: {state['age']}
Symptoms: {state['symptoms']}
History: {state['history']}

Return ONLY valid JSON. No explanation.

Format:
{{
    "disease": "...",
    "severity": "...",
    "treatment": "...",
    "reason": "..."
}}
"""

    # 🔥 SMART API + FALLBACK
    if client:
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
                timeout=20
            )

            output_text = response.choices[0].message.content.strip()

        except Exception as e:
            print(f"[STEP] API Error: {e}")

            # fallback if API fails
            output_text = json.dumps({
                "disease": "possible condition",
                "severity": "medium",
                "treatment": "consult doctor",
                "reason": "API failed, using fallback"
            })
    else:
        # 🚀 NO API → DEMO MODE
        print("[STEP] Running in demo mode (no API key)")

        # simple logic-based fallback
        symptoms = " ".join(state["symptoms"]).lower()

        if "chest pain" in symptoms:
            disease = "Heart Disease"
        elif "fever" in symptoms:
            disease = "Infection"
        elif "thirst" in symptoms or "urination" in symptoms:
            disease = "Diabetes"
        else:
            disease = "General illness"

        output_text = json.dumps({
            "disease": disease,
            "severity": "medium",
            "treatment": "consult doctor",
            "reason": "Rule-based demo prediction"
        })

    print(f"[STEP] Model Output: {output_text}")

    # SAFE JSON PARSING
    try:
        action = json.loads(output_text)
    except:
        action = {
            "disease": "unknown",
            "severity": "uncertain",
            "treatment": "consult doctor",
            "reason": "parsing failed"
        }

    result = env.step(action)

    print(f"[STEP] Reward: {result['reward']}")

    total_reward += result["reward"]

avg_score = total_reward / num_cases

print(f"[END] Average Score: {avg_score}")
