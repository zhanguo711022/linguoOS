from __future__ import annotations

from dataclasses import asdict

from fastapi import APIRouter, Depends, Query

from linguoos.api.deps import get_repo
from linguoos.storage.sqlite import SQLiteRepository

router = APIRouter(prefix="/history", tags=["history"])


@router.get("/recent")
async def recent_history(
    session_id: str = Query(...),
    limit: int = Query(20, ge=1, le=100),
    repo: SQLiteRepository = Depends(get_repo),
):
    records = await repo.list_records(session_id=session_id, limit=limit)
    return {"ok": True, "data": [asdict(item) for item in records]}


@router.delete("/clear")
async def clear_history(session_id: str = Query(...)):
    return {"ok": True, "data": {"session_id": session_id, "cleared": False}}
