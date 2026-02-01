from fastapi import APIRouter

from linguoos.orchestrator.core import Orchestrator
from linguoos.schemas.decision import DecisionInput, OrchestratorDecision

router = APIRouter(prefix="/api/v1/decision", tags=["decision"])


@router.post("/next", response_model=OrchestratorDecision)
def next_step(inp: DecisionInput) -> OrchestratorDecision:
    """Return the next action from a placeholder orchestrator decision."""
    orch = Orchestrator()
    return orch.decide_next_action(profile=None, workspace_state=None, decision_input=inp)
