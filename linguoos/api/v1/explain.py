from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from linguoos.api.deps import get_explain_service
from linguoos.schemas.explain import Explanation
from linguoos.services.explain_service import ExplainService

router = APIRouter(prefix="/explain", tags=["explain"])


@router.get("/concept", response_model=Explanation)
async def explain_concept(
    session_id: str = Query(...),
    concept: str = Query(...),
    level: str | None = Query(None),
    service: ExplainService = Depends(get_explain_service),
):
    result = await service.explain(session_id=session_id, concept=concept, level=level)
    return Explanation(**result)
