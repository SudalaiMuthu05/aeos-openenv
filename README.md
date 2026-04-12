---
title: AEOS Environment
emoji: 🚀
colorFrom: blue
colorTo: green
sdk: docker
app_file: app.py
pinned: false
---

# 🚀 AEOS: Autonomous Enterprise Operations Simulator

AEOS is a **production-grade autonomous environment** designed to simulate and evaluate enterprise-level operational workflows. Built for the OpenEnv ecosystem, it combines structured simulation, intelligent agents, and robust evaluation mechanisms.

---

## 🏗️ Project Architecture

AEOS/
├── app.py # FastAPI server (API layer)
├── inference.py # Intelligent agent (LLM + rules)
├── openenv.yaml # OpenEnv compliance specification
├── Dockerfile # Deployment container (HF compatible)
├── requirements.txt # Dependencies
└── env/
├── environment.py # Core simulation engine
├── models.py # Data schemas (Pydantic)
├── tasks.py # Task definitions (Easy/Medium/Hard)
└── graders.py # Deterministic evaluation logic


---

## 🧠 Key Features

### 🔹 Dynamic State Management
- Tracks emails, tickets, agent workloads, and SLA deadlines in real-time  
- Maintains evolving system state across steps  

### 🔹 Advanced Reward Engineering
- Immediate action rewards  
- Efficiency-based incentives  
- Long-term system stability bonuses  

### 🔹 SLA-Aware Simulation
- Time-decay penalties for delayed tasks  
- Encourages prioritization and urgency handling  

### 🔹 OpenEnv Compliant
- Fully compatible with `openenv validate`  
- Strict API contract: `/reset`, `/step`, `/state`  
- Standardized logging (`[START]`, `[STEP]`, `[END]`)  

### 🔹 Production Ready
- Dockerized for Hugging Face Spaces  
- Stateless API design  
- Scalable and modular architecture  

---

## 🌐 Decision Intelligence

AEOS implements a **hybrid intelligent agent system**:

- 🔹 Rule-based prioritization for SLA-sensitive tasks  
- 🔹 LLM-based reasoning via OpenAI proxy (LiteLLM compliant)  
- 🔹 Dynamic workload balancing across agents  
- 🔹 Anti-loop and stability-aware execution  

This ensures:
> realistic, consistent, and high-quality enterprise decision-making

---

## 🧪 Evaluation System

AEOS evaluates performance across three difficulty tiers:

| Level | Task | Description |
|------|------|-------------|
| 🟢 Easy | Triage | Classification of incoming emails/tickets |
| 🟡 Medium | Resolution | Responding to tasks efficiently |
| 🔴 Hard | Ops Management | SLA handling + workload balancing |

---

## 🚀 Getting Started

### 1. Install Dependencies
python -m pip install -r requirements.txt

### 2. Run the Server
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload

### 3. Execute Inference
python inference.py

## 🐳 Docker Deployment
docker build -t aeos-env .
docker run -p 7860:7860 aeos-env


## 🏆 Why AEOS Stands Out
Hybrid LLM + rule-based intelligence
Real-world SLA-driven simulation
Strong reward shaping for RL evaluation
Fully OpenEnv-compliant architecture
Designed for scalability and realism

## 📌 Summary

AEOS is not just a simulation — it is a decision-making system that models real enterprise workflows with intelligence, adaptability, and precision.

---
