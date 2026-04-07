from pydantic import BaseModel
from typing import List, Dict, Optional


# -----------------------------
# Email / Ticket Models
# -----------------------------

class Email(BaseModel):
    id: str
    content: str
    priority: str  # low / medium / high
    resolved: bool = False


class Ticket(BaseModel):
    id: str
    issue: str
    severity: str  # low / medium / high
    assigned_to: Optional[str] = None
    resolved: bool = False


class AgentStatus(BaseModel):
    name: str
    workload: int  # number of tasks assigned


# -----------------------------
# State (FULL INTERNAL STATE)
# -----------------------------

class AEOSState(BaseModel):
    emails: List[Email]
    tickets: List[Ticket]
    agents: Dict[str, AgentStatus]
    sla_deadlines: Dict[str, int]
    time_step: int
    history: List[str]


# -----------------------------
# Observation (VISIBLE TO AGENT)
# -----------------------------

class AEOSObservation(BaseModel):
    pending_emails: List[str]
    pending_tickets: List[str]
    urgency_levels: Dict[str, str]
    team_load: Dict[str, int]
    last_feedback: str


# -----------------------------
# Action (AGENT INPUT)
# -----------------------------

class AEOSAction(BaseModel):
    action_type: str  # classify / respond / assign / escalate
    target_id: Optional[str] = None
    content: Optional[str] = None


# -----------------------------
# Step Result (ENV OUTPUT)
# -----------------------------

class AEOSStepResult(BaseModel):
    observation: AEOSObservation
    reward: float
    done: bool
    info: Dict = {}
