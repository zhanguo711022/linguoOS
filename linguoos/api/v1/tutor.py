from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

from linguoos.services.ai_tutor_service import get_ai_tutor

router = APIRouter(prefix="/api/v1/tutor", tags=["tutor"])


class TutorExplainRequest(BaseModel):
    question: str
    wrong_answer: str = Field(..., min_length=1)
    correct_answer: str = Field(..., min_length=1)
    module_id: str = "general"
    language: str = "en"


class TutorChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    history: list[dict[str, Any]] = Field(default_factory=list)
    module_id: str = "general"


@router.post("/explain")
async def explain_wrong_answer(payload: TutorExplainRequest) -> dict:
    service = get_ai_tutor()
    return await service.explain_wrong_answer(
        question=payload.question,
        wrong_answer=payload.wrong_answer,
        correct_answer=payload.correct_answer,
        module_id=payload.module_id,
        language=payload.language,
    )


@router.post("/chat")
async def chat(payload: TutorChatRequest) -> dict:
    service = get_ai_tutor()
    return await service.chat(
        message=payload.message,
        history=payload.history,
        module_id=payload.module_id,
    )
