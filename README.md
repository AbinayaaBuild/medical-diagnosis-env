---
title: Medical Diagnosis AI
emoji: 🏥
colorFrom: blue
colorTo: green
sdk: docker
app_file: baseline/baseline.py
pinned: false
tags:
- openenv
---

# 🏥 AI Medical Diagnosis Simulator

## 🧠 Description
This project is an AI-powered medical diagnosis simulator built using an OpenEnv-style environment. It enables an AI agent to interact with a structured environment to diagnose diseases based on patient symptoms and medical history.

The system is designed to evaluate decision-making ability, reasoning, and consistency of AI agents in a realistic healthcare scenario.

---

## 🎯 Motivation
Medical diagnosis is a critical real-world task that requires reasoning over symptoms, patient history, and uncertainty. This project simulates such decision-making to evaluate AI agents in a structured, reproducible, and measurable way.

It aims to bridge the gap between simple toy environments and real-world agent evaluation tasks.

---

## ⚙️ How it Works
The system follows an environment-based interaction model:

- `reset()` → Initializes a new patient case  
- `state()` → Returns the full internal state (ground truth)  
- `get_state()` → Returns observable patient data  
- `step(action)` → Evaluates prediction and returns reward  

---

## 🎮 Action Space
The agent must output:

- `disease` (string)  
- `severity` (string)  
- `treatment` (string)  
- `reason` (string)  

---

## 👁️ Observation Space
The agent receives:

- `age` (integer)  
- `symptoms` (list of strings)  
- `history` (list of strings)  

---

## 🧪 Tasks (Difficulty Levels)

The environment defines three structured task categories:

### 🟢 Easy Task
- Common cold  
- Allergy  
- Flu  
👉 Requires basic symptom recognition

### 🟡 Medium Task
- Diabetes  
- Dengue  
- Food poisoning  
👉 Requires combining multiple symptoms for diagnosis

### 🔴 Hard Task
- Stroke  
- Heart attack  
- Alzheimer’s  
👉 Requires reasoning over symptoms + patient history (complex decision-making)

---

## 🧮 Reward Function

The environment provides a **dense and interpretable reward signal**:

- Disease match → **0.4**  
- Severity match → **0.2**  
- Treatment match → **0.2**  
- Reason correctness → **0.2**  

Total reward ranges from **0.0 to 1.0**, enabling partial credit and fine-grained evaluation.

---

## 📊 Baseline Performance

The rule-based baseline agent achieves:

- **Average Score: 1.0** across test cases  
- Deterministic and reproducible results  
- Strong performance across all difficulty levels  

---

## 📁 Project Structure

- `env/environment.py` → Environment logic  
- `baseline/baseline.py` → Baseline agent logic  
- `dataset/medical_cases.json` → Dataset  
- `openenv.yaml` → Environment configuration  
- `Dockerfile` → Container setup  

---

## ▶️ How to Run

```bash
python baseline/baseline.py

----

## 🏁 Result

The system successfully evaluates multiple patient cases and produces accurate diagnoses using a structured reward mechanism. It demonstrates strong performance, reproducibility, and suitability for evaluating AI agents.
