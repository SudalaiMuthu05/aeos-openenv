from typing import Dict


TASKS = {
    "triage_easy": {
        "description": "Classify emails and tickets correctly based on priority/severity",
        "max_steps": 5
    },
    "resolution_medium": {
        "description": "Respond appropriately to emails and tickets",
        "max_steps": 7
    },
    "ops_hard": {
        "description": "Manage tasks, assign agents, and meet SLA deadlines efficiently",
        "max_steps": 10
    }
}
