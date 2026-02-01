from typing import Dict, List, Optional

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/workspace", tags=["workspace"])


class Module(BaseModel):
    id: str
    name: str


class AbilitySnapshot(BaseModel):
    stage: int
    core_issue: str
    dimensions: Dict[str, Dict[str, Optional[str | int]]]


class WorkspaceContext(BaseModel):
    current_module: Module
    ability_snapshot: AbilitySnapshot
    allowed_actions: List[str]


@router.get("/context", response_model=WorkspaceContext)
def get_workspace_context() -> WorkspaceContext:
    return WorkspaceContext(
        current_module=Module(id="precision.generalization", name="Generalization"),
        ability_snapshot=AbilitySnapshot(
            stage=2,
            core_issue="precision",
            dimensions={
                "precision": {"level": 54, "trend": "up"},
                "structure": {"level": 68, "trend": "steady"},
            },
        ),
        allowed_actions=["submit_task", "continue_practice"],
    )
