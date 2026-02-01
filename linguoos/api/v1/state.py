from fastapi import APIRouter, Query

from linguoos.schemas.state import WorkspaceState

router = APIRouter(prefix="/api/v1/state", tags=["state"])


@router.get("/current", response_model=WorkspaceState)
def get_current_state(user_id: str = Query(...)) -> WorkspaceState:
    return WorkspaceState(
        user_id=user_id,
        active_task_id="mock-task-001",
        progress={"phase": "mock", "status": "idle"},
    )
