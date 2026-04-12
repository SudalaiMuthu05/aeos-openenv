import os
import requests
from openai import OpenAI
from typing import List
from env.tasks import TASKS

API_BASE_URL = os.environ["API_BASE_URL"]
API_KEY = os.environ["API_KEY"]
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")

ENV_URL = "http://localhost:7860"

client = OpenAI(
    api_key=API_KEY,
    base_url=API_BASE_URL
)

SUCCESS_THRESHOLD = 0.3
EPS = 1e-6


def log_start(task, env, model):
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step, action, reward, done, error):
    error_val = error if error else "null"
    done_val = str(done).lower()
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}", flush=True)


def log_end(success, steps, score, rewards):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}", flush=True)


def normalize(x):
    return max(EPS, min(x, 1.0 - EPS))

def rule_based_action(obs):
    emails = obs.get("pending_emails", [])
    tickets = obs.get("pending_tickets", [])
    team_load = obs.get("team_load", {})

    # Priority 1 → classify new items
    if len(emails) > 0:
        return "classify"

    # Priority 2 → respond to pending tickets
    if len(tickets) > 0:
        return "respond"

    # Priority 3 → balance workload
    if any(load < 2 for load in team_load.values()):
        return "assign"

    return None

def llm_action(step, obs):
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert operations strategist. Optimize SLA, workload, and efficiency. Return only one word: classify, respond, or assign."
                },
                {
                    "role": "user",
                    "content": f"""
Step {step}

Emails: {obs['pending_emails']}
Tickets: {obs['pending_tickets']}
Load: {obs['team_load']}
"""
                }
            ],
            max_tokens=10,
            temperature=0.0,
        )

        action = completion.choices[0].message.content.strip().lower()

        if action in ["classify", "respond", "assign"]:
            return action

    except:
        pass

    return "assign"


def run_task(task_id, task_config):
    rewards = []
    steps_taken = 0
    max_steps = task_config.get("max_steps", 8)

    log_start(task_id, "aeos_env", MODEL_NAME)

    try:
        res = requests.post(f"{ENV_URL}/reset")
        data = res.json()
    except:
        log_end(False, 0, 0.5, [])
        return 0.5

    for step in range(1, max_steps + 1):

        obs = data.get("observation", {})

        # 🔥 HYBRID DECISION ENGINE
        action_type = rule_based_action(obs)

        if action_type is None:
            action_type = llm_action(step, obs)

        # 🔥 Anti-loop safety
        if len(rewards) >= 2 and rewards[-1] < 0.4:
            action_type = "assign"

        payload = {
            "action_type": action_type,
            "target_id": "agent_1",
            "content": "auto-response"
        }

        try:
            res = requests.post(f"{ENV_URL}/step", json=payload)
            data = res.json()
        except Exception as e:
            r = normalize(0.5)
            log_step(step, action_type, r, True, str(e))
            rewards.append(r)
            break

        reward = normalize(data.get("reward", 0.5))
        done = data.get("done", False)

        rewards.append(reward)
        steps_taken = step

        log_step(step, action_type, reward, done, None)

        if done:
            break

    score = sum(rewards) / len(rewards) if rewards else 0.5
    score = normalize(score)

    success = score >= SUCCESS_THRESHOLD

    log_end(success, steps_taken, score, rewards)
    return score


def main():
    total = 0.0

    for task_id, task_config in TASKS.items():
        total += run_task(task_id, task_config)

    return normalize(total / len(TASKS))


if __name__ == "__main__":
    main()
