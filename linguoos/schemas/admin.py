from __future__ import annotations

from pydantic import BaseModel


class StudentProgress(BaseModel):
    user_id: str
    sessions: int
    last_session_id: str | None = None


class InterventionRecord(BaseModel):
    id: int
    session_id: str
    reason: str
    status: str
    teacher_response: str | None = None
