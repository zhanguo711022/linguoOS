from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class TaskSubmissionRequest(BaseModel):
    """Practice submission payload.

    NOTE: This model is intentionally permissive and backward-compatible.
    We keep /api/v1/* contracts stable while allowing older/newer clients.
    """

    user_id: str = Field(..., description="Identifier for the user.")

    # Optional: some clients attach a task_id; others don't.
    task_id: Optional[str] = Field(None, description="Identifier for the task (optional).")

    # Common fields used by the UI/demo/verify scripts.
    input_type: Optional[str] = Field(None, description="Input type (optional, e.g. text)")
    client_context: Dict[str, Any] = Field(default_factory=dict)

    payload: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        extra = "allow"
