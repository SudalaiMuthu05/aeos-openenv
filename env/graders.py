from typing import List
from env.models import AEOSState

# -----------------------------
# GLOBAL NORMALIZER (STRICT)
# -----------------------------
def normalize(score: float) -> float:
    EPS = 1e-6

    # Handle None / NaN safety
    if score is None:
        return 0.5

    # Clamp strictly inside (0,1)
    score = max(EPS, min(score, 1.0 - EPS))

    return score


# -----------------------------
# EASY TASK GRADER
# -----------------------------
def grade_triage(state: AEOSState, history: List[str]) -> float:
    score = 0.0

    # classification reward
    classify_actions = [h for h in history if "classify" in h]
    if len(classify_actions) > 0:
        score += 0.5

    # no invalid actions reward
    invalid_actions = [h for h in history if "Invalid" in h]
    if len(invalid_actions) == 0:
        score += 0.5

    # 🔥 EDGE CASE: no history → neutral score
    if len(history) == 0:
        return normalize(0.5)

    return normalize(score)


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

    # 🔥 EDGE CASE: no actions
    if len(history) == 0:
        return normalize(0.5)

    return normalize(score)


# -----------------------------
# HARD TASK GRADER
# -----------------------------
def grade_ops(state: AEOSState, history: List[str]) -> float:
    score = 0.0

    # -------------------------
    # Workload Balance
    # -------------------------
    workloads = [agent.workload for agent in state.agents.values()]

    if len(workloads) > 0:
        if max(workloads) > 0:
            balance = min(workloads) / max(workloads)
        else:
            balance = 1.0

        score += 0.3 * balance

    # -------------------------
    # SLA Success
    # -------------------------
    sla_success = sum(1 for v in state.sla_deadlines.values() if v >= 0)
    total_sla = len(state.sla_deadlines)

    if total_sla > 0:
        score += 0.4 * (sla_success / total_sla)

    # -------------------------
    # Action Diversity
    # -------------------------
    unique_actions = set(history)
    score += 0.3 * (len(unique_actions) / 4)

    # 🔥 EDGE CASE: no activity
    if len(history) == 0:
        return normalize(0.5)

    return normalize(score)
