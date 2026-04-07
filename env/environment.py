from typing import Dict, List
from env.models import (
    AEOSState,
    AEOSObservation,
    AEOSAction,
    AEOSStepResult,
    Email,
    Ticket,
    AgentStatus,
)


class AEOSEnv:

    def __init__(self):
        self.state_data: AEOSState = None
        self.max_steps = 10

    # -----------------------------
    # RESET
    # -----------------------------
    def reset(self) -> AEOSObservation:
        emails = [
            Email(id="email_1", content="Need refund urgently", priority="high"),
            Email(id="email_2", content="General inquiry", priority="low"),
        ]

        tickets = [
            Ticket(id="ticket_1", issue="Login not working", severity="high"),
            Ticket(id="ticket_2", issue="UI bug", severity="medium"),
        ]

        agents = {
            "agent_1": AgentStatus(name="agent_1", workload=0),
            "agent_2": AgentStatus(name="agent_2", workload=0),
        }

        sla_deadlines = {
            "email_1": 2,
            "ticket_1": 3,
        }

        self.state_data = AEOSState(
            emails=emails,
            tickets=tickets,
            agents=agents,
            sla_deadlines=sla_deadlines,
            time_step=0,
            history=[],
        )

        return self._get_observation("Environment reset")

    # -----------------------------
    # STEP
    # -----------------------------
    def step(self, action: AEOSAction) -> AEOSStepResult:
        reward = 0.0
        done = False
        feedback = ""

        self.state_data.time_step += 1
        self.state_data.history.append(action.action_type)

        # ---- BASE REWARD ----
        if action.action_type == "classify":
            reward += 0.2
            feedback = "Classification done"

        elif action.action_type == "respond":
            reward += 0.3
            feedback = "Response sent"

        elif action.action_type == "assign":
            if action.target_id in self.state_data.agents:
                self.state_data.agents[action.target_id].workload += 1
                reward += 0.25

                # efficiency bonus
                if self.state_data.agents[action.target_id].workload < 3:
                    reward += 0.1

                feedback = "Task assigned"
            else:
                reward -= 0.5
                feedback = "Invalid agent"

        elif action.action_type == "escalate":
            reward += 0.15
            feedback = "Escalated"

        else:
            reward -= 0.5
            feedback = "Invalid action"

        # ---- SLA DECAY ----
        for key in list(self.state_data.sla_deadlines.keys()):
            self.state_data.sla_deadlines[key] -= 1

            if self.state_data.sla_deadlines[key] < 0:
                reward -= 0.1 * abs(self.state_data.sla_deadlines[key])

        # ---- SYSTEM STABILITY BONUS ----
        if all(v >= 0 for v in self.state_data.sla_deadlines.values()):
            reward += 0.2

        # ---- DONE CONDITION ----
        if self.state_data.time_step >= self.max_steps:
            done = True

        observation = self._get_observation(feedback)

        return AEOSStepResult(
            observation=observation,
            reward=max(min(reward, 1.0), -1.0),
            done=done,
            info={}
        )

    # -----------------------------
    # STATE
    # -----------------------------
    def state(self) -> AEOSState:
        return self.state_data

    # -----------------------------
    # OBSERVATION HELPER
    # -----------------------------
    def _get_observation(self, feedback: str) -> AEOSObservation:
        pending_emails = [e.id for e in self.state_data.emails if not e.resolved]
        pending_tickets = [t.id for t in self.state_data.tickets if not t.resolved]

        urgency_levels = {}
        for e in self.state_data.emails:
            urgency_levels[e.id] = e.priority
        for t in self.state_data.tickets:
            urgency_levels[t.id] = t.severity

        team_load = {
            agent: self.state_data.agents[agent].workload
            for agent in self.state_data.agents
        }

        return AEOSObservation(
            pending_emails=pending_emails,
            pending_tickets=pending_tickets,
            urgency_levels=urgency_levels,
            team_load=team_load,
            last_feedback=feedback
        )
