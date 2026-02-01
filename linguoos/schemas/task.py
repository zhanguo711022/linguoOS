from typing import Any, Dict

from pydantic import BaseModel, Field


class TaskSubmissionRequest(BaseModel):
    user_id: str = Field(..., description="Identifier for the user.")
    task_id: str = Field(..., description="Identifier for the task.")
    payload: Dict[str, Any] = Field(default_factory=dict)
