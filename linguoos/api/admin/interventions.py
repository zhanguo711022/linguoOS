from __future__ import annotations

from fastapi import APIRouter, Depends

from linguoos.api.deps import get_intervention_service, get_repo
from linguoos.core.domain import LearningRecord
from linguoos.schemas.admin import InterventionRecord
from linguoos.services.intervention_service import InterventionService
from linguoos.storage.sqlite import SQLiteRepository

router = APIRouter(prefix="/admin/interventions", tags=["admin-interventions"])


@router.get("")
async def list_interventions(
    status: str | None = None,
    repo: SQLiteRepository = Depends(get_repo),
):
    items = await repo.list_interventions(status=status)
    return {"ok": True, "data": [InterventionRecord(**item).model_dump() for item in items]}


@router.post("/{intervention_id}/respond")
async def respond_intervention(
    intervention_id: int,
    payload: dict,
    repo: SQLiteRepository = Depends(get_repo),
    service: InterventionService = Depends(get_intervention_service),
):
    response_text = payload.get("response", "")
    await service.resolve(intervention_id, response_text)
    session_id = payload.get("session_id")
    if session_id:
        await repo.add_record(
            LearningRecord(
                session_id=session_id,
                action_type="teacher_response",
                payload={"response": response_text},
                correct=None,
            )
        )
    return {"ok": True, "data": {"resolved": True}}
