from __future__ import annotations

from dataclasses import asdict

from fastapi import APIRouter, Depends, HTTPException

from linguoos.api.deps import get_session_service
from linguoos.schemas.session import SessionMessage, SessionMessageResponse, SessionResponse, SessionStart
from linguoos.services.session_service import SessionService

router = APIRouter(prefix="/session", tags=["session"])


@router.post("/start", response_model=SessionResponse)
async def start_session(payload: SessionStart, service: SessionService = Depends(get_session_service)):
    result = await service.start(user_id=payload.user_id, language=payload.language)
    return SessionResponse(**result)


@router.post("/message", response_model=SessionMessageResponse)
async def message_session(payload: SessionMessage, service: SessionService = Depends(get_session_service)):
    try:
        result = await service.handle_message(session_id=payload.session_id, message=payload.message)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return SessionMessageResponse(**result)


@router.get("/{session_id}/history")
async def get_history(session_id: str, service: SessionService = Depends(get_session_service)):
    records = await service.history(session_id)
    return {"ok": True, "data": [asdict(item) for item in records]}
