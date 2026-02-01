from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class WorkspaceState(BaseModel):
    user_id: str = Field(..., description="Identifier for the user.")
    active_task_id: Optional[str] = Field(default=None)
    progress: Dict[str, Any] = Field(default_factory=dict)


class GrowthOverview(BaseModel):
    user_id: str = Field(..., description="Identifier for the user.")
    milestones: List[str] = Field(default_factory=list)
    summary: str = Field(..., description="Mock overview summary.")
