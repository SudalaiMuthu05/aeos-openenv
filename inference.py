import os
import requests
from openai import OpenAI
from typing import List
from env.tasks import TASKS

# -----------------------------
# CONFIG
# -----------------------------

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

# Minimal safe compliance: initialize the OpenAI client
client = OpenAI(api_key=HF_TOKEN, base_url=API_BASE_URL)

SUCCESS_THRESHOLD = 0.3


# -----------------------------
# LOGGING (STRICT FORMAT)
# -----------------------------

def log_start(task, env, model):
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step, action, reward, done, error):
    error_val = error if error else "null"
    done_val = str(done).lower()
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}",
        flush=True,
    )


def log_end(success, steps, score, rewards):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}",
        flush=True,
    )


# -----------------------------
# SIMPLE AGENT (BASELINE)
# -----------------------------

def choose_action(step):
    # simple deterministic baseline
    if step % 3 == 0:
        return "assign"
    elif step % 2 == 0:
        return "respond"
    else:
        return "classify"


# -----------------------------
# MAIN LOOP
# -----------------------------

def run_task(task_id, task_config):
    rewards = []
    steps_taken = 0
    max_steps = task_config.get("max_steps", 8)

    log_start(task=task_id, env="aeos_env", model=MODEL_NAME)

    # reset env
    try:
        res = requests.post(f"{API_BASE_URL}/reset")
        res.raise_for_status()
        obs = res.json()
    except Exception as e:
        log_end(False, 0, 0.0, [])
        return 0.0

    for step in range(1, max_steps + 1):

        action_type = choose_action(step)

        action_payload = {
            "action_type": action_type,
            "target_id": "agent_1",
            "content": "auto-response"
        }

        try:
            res = requests.post(f"{API_BASE_URL}/step", json=action_payload)
            res.raise_for_status()
            data = res.json()
        except Exception as e:
            log_step(step, action_type, 0.0, True, str(e))
            break

        reward = data.get("reward", 0.0)
        done = data.get("done", False)

        rewards.append(reward)
        steps_taken = step

        log_step(step, action_type, reward, done, None)

        if done:
            break

    # normalize score
    score = sum(rewards) / len(rewards) if rewards else 0.0
    score = min(max(score, 0.0), 1.0)

    success = score >= SUCCESS_THRESHOLD

    log_end(success, steps_taken, score, rewards)
    return score


def main():
    total_score = 0.0
    for task_id, task_config in TASKS.items():
        total_score += run_task(task_id, task_config)
    
    total_score / len(TASKS) if TASKS else 0.0


if __name__ == "__main__":
    main()
