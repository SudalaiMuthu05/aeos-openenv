---
title: AEOS Environment
emoji: 🚀
colorFrom: blue
colorTo: green
sdk: docker
app_file: app.py
pinned: false
---

# AEOS: Autonomous Enterprise Operations Simulator 🚀

AEOS is a production-grade, autonomous environment for simulating and evaluating enterprise-level operational workflows. Designed for the OpenEnv ecosystem, it features a robust FastAPI backend, deterministic reward shaping, and multi-tier task evaluation.

## 🏗️ Project Architecture

```text
AEOS/
├── app.py              # FastAPI server (API layer)
├── inference.py        # Automated agent runner (Inference layer)
├── openenv.yaml        # OpenEnv compliance specification
├── Dockerfile          # Scalable deployment container
├── requirements.txt    # Dependency manifest
└── env/
    ├── environment.py  # Core simulation logic & state machine
    ├── models.py       # Pydantic data schemas
    ├── tasks.py        # Task difficulty definitions
    └── graders.py      # Deterministic evaluation algorithms
```

## 🧠 Key Features

- **Dynamic State Management:** Tracks real-time emails, tickets, and agent workloads.
- **Advanced Reward Engineering:** Multi-faceted rewards including immediate action signals, efficiency bonuses, and long-term system stability incentives.
- **SLA Decay Simulation:** Realistic time-sensitive penalties for pending tasks.
- **OpenEnv Compliant:** Fully supports `openenv validate` and standardized logging formats.
- **Production-Ready:** Includes Docker support for seamless deployment to platforms like Hugging Face Spaces.

## 🚀 Getting Started

### 1. Install Dependencies
```bash
python -m pip install -r requirements.txt
```

### 2. Run the Server
```bash
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Execute Inference & Scoring
```bash
python inference.py
```

## 🌐 Decision Intelligence

AEOS uses a hybrid decision engine:

- Rule-based prioritization for SLA-sensitive tasks  
- LLM-based reasoning for adaptive decisions  
- Dynamic workload balancing  
- Anti-loop stability mechanism  

This ensures consistent and realistic enterprise simulation.

## 🧪 Evaluation System

AEOS evaluates agents across three difficulty levels:
- **Triage (Easy):** Correct classification of incoming data.
- **Resolution (Medium):** Proficiency in responding to entities.
- **Ops Management (Hard):** Balancing workloads and mastering SLA deadlines.

## 🐳 Docker Deployment

Build and run your container locally:
```bash
docker build -t aeos-env .
docker run -p 7860:7860 aeos-env
```
