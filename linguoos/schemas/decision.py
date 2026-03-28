from __future__ import annotations

from pydantic import BaseModel


class DecisionInput(BaseModel):
    session_id: str


class OrchestratorDecision(BaseModel):
    action: str
    reason: str
    confidence: float
