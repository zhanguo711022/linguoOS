from __future__ import annotations

from fastapi import APIRouter, Depends

from linguoos.api.deps import get_repo
from linguoos.schemas.admin import StudentProgress
from linguoos.storage.sqlite import SQLiteRepository

router = APIRouter(prefix="/admin/students", tags=["admin-students"])


@router.get("")
async def list_students(repo: SQLiteRepository = Depends(get_repo)):
    sessions = await repo.list_sessions()
    by_user: dict[str, list[str]] = {}
    for session in sessions:
        by_user.setdefault(session.user_id, []).append(session.session_id)
    return {
        "ok": True,
        "data": [
            StudentProgress(
                user_id=user_id,
                sessions=len(session_ids),
                last_session_id=session_ids[-1] if session_ids else None,
            ).model_dump()
            for user_id, session_ids in by_user.items()
        ],
    }


@router.get("/{user_id}/progress", response_model=StudentProgress)
async def student_progress(user_id: str, repo: SQLiteRepository = Depends(get_repo)):
    sessions = await repo.list_sessions_by_user(user_id)
    last_session_id = sessions[-1].session_id if sessions else None
    return StudentProgress(user_id=user_id, sessions=len(sessions), last_session_id=last_session_id)
