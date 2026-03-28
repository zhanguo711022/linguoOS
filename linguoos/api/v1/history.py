from typing import Optional

from fastapi import APIRouter, Query

from linguoos.storage.sqlite import clear_attempts, recent_attempts

router = APIRouter(prefix="/api/v1/history", tags=["history"])


@router.get("/recent")
def recent(user_id: Optional[str] = Query(None), limit: int = Query(20, ge=1, le=200)):
    return {"items": recent_attempts(user_id, limit)}


@router.delete("/clear")
def clear(user_id: Optional[str] = Query(None)):
    clear_attempts(user_id)
    return {"ok": True}
