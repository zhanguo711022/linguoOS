from __future__ import annotations

from pydantic import BaseModel


class SessionStart(BaseModel):
    user_id: str
    language: str | None = None


class SessionMessage(BaseModel):
    session_id: str
    message: str


class SessionResponse(BaseModel):
    session_id: str
    welcome_message: str
    first_action: str


class SessionMessageResponse(BaseModel):
    reply: str
    next_action: str
    feedback: dict | None = None
    intervention_flagged: bool = False
