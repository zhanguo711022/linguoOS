from enum import Enum

from pydantic import BaseModel


class Action(str, Enum):
    practice = "practice"
    feedback = "feedback"
    explain = "explain"
    complete = "complete"


class DecisionInput(BaseModel):
    user_id: str
    module_id: str = "precision.generalization"
    last_mode: str | None = None
    last_correct: bool | None = None


class OrchestratorDecision(BaseModel):
    action: Action
    target_module: str
    reason: str
