from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query

from linguoos.api.deps import get_practice_service
from linguoos.schemas.practice import FeedbackResponse, PracticeItem, SubmitRequest
from linguoos.services.practice_service import PracticeService

router = APIRouter(prefix="/practice", tags=["practice"])


@router.get("/next", response_model=PracticeItem)
async def next_practice(
    session_id: str = Query(...),
    module_id: str = Query("grammar"),
    service: PracticeService = Depends(get_practice_service),
):
    item = await service.next_item(session_id=session_id, module_id=module_id)
    return PracticeItem(**item)


@router.post("/submit", response_model=FeedbackResponse)
async def submit_practice(payload: SubmitRequest, service: PracticeService = Depends(get_practice_service)):
    if not payload.answer:
        raise HTTPException(status_code=400, detail="answer required")
    result = await service.submit(
        session_id=payload.session_id,
        prompt=payload.prompt,
        answer=payload.answer,
        expected_answer=payload.expected_answer,
    )
    return FeedbackResponse(**result)
