from __future__ import annotations

from fastapi import APIRouter

from linguoos.schemas.profile import ProfileCore

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("")
async def get_profile():
    return {"ok": True, "data": ProfileCore().model_dump()}


@router.put("")
async def update_profile(payload: ProfileCore):
    return {"ok": True, "data": payload.model_dump()}
