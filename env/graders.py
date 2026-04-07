from typing import List
from env.models import AEOSState


# -----------------------------
# EASY TASK GRADER
# -----------------------------
def grade_triage(state: AEOSState, history: List[str]) -> float:
    score = 0.0

    # reward if classification actions exist
    classify_actions = [h for h in history if "classify" in h]

    if len(classify_actions) > 0:
        score += 0.5

    # reward if no invalid actions
    invalid_actions = [h for h in history if "Invalid" in h]
    if len(invalid_actions) == 0:
        score += 0.5

    return min(score, 1.0)


# -----------------------------
# MEDIUM TASK GRADER
# -----------------------------
def grade_resolution(state: AEOSState, history: List[str]) -> float:
    score = 0.0

    responses = [h for h in history if "respond" in h]

    if len(responses) > 0:
        score += 0.5

    if len(responses) >= 2:
        score += 0.3

    if all("Invalid" not in h for h in history):
        score += 0.2

    return min(score, 1.0)


# -----------------------------
# HARD TASK GRADER (🔥 IMPORTANT)
# -----------------------------
def grade_ops(state: AEOSState, history: List[str]) -> float:
    score = 0.0

    # workload balance
    workloads = [agent.workload for agent in state.agents.values()]
    if len(workloads) > 0:
        # Check if max(workloads) > 0 to avoid ZeroDivisionError
        if max(workloads) > 0:
            balance = min(workloads) / max(workloads)
        else:
            balance = 1.0
        score += 0.3 * balance

    # SLA success
    sla_success = sum(1 for v in state.sla_deadlines.values() if v >= 0)
    total_sla = len(state.sla_deadlines)

    if total_sla > 0:
        score += 0.4 * (sla_success / total_sla)

    # action diversity
    unique_actions = set(history)
    score += 0.3 * (len(unique_actions) / 4)

    return min(score, 1.0)
