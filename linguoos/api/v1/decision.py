from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from linguoos.api.deps import get_orchestrator, get_repo
from linguoos.core.orchestrator import OrchestratorV2
from linguoos.schemas.decision import DecisionInput, OrchestratorDecision
from linguoos.storage.sqlite import SQLiteRepository

router = APIRouter(prefix="/decision", tags=["decision"])


@router.post("/next", response_model=OrchestratorDecision)
async def next_decision(
    payload: DecisionInput,
    repo: SQLiteRepository = Depends(get_repo),
    orchestrator: OrchestratorV2 = Depends(get_orchestrator),
):
    session = await repo.get_session(payload.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="session not found")
    history = await repo.list_records(payload.session_id, limit=20)
    decision = orchestrator.decide(history, {})
    return OrchestratorDecision(action=decision.action, reason=decision.reason, confidence=decision.confidence)
