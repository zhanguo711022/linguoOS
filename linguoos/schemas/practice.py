from __future__ import annotations

from pydantic import BaseModel


class PracticeItem(BaseModel):
    id: str
    module_id: str
    prompt: str
    expected_answer: str | None = None
    difficulty: str | None = None


class SubmitRequest(BaseModel):
    session_id: str
    prompt: str
    answer: str
    expected_answer: str | None = None


class FeedbackResponse(BaseModel):
    correct: bool
    score: float
    feedback: dict
