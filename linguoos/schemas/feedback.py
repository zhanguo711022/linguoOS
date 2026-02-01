from typing import Any, Dict, List

from pydantic import BaseModel, Field


class FeedbackBlock(BaseModel):
    block_id: str = Field(..., description="Identifier for the feedback block.")
    message: str = Field(..., description="Feedback message placeholder.")
    metadata: Dict[str, Any] = Field(default_factory=dict)


class FeedbackResponse(BaseModel):
    submission_id: str = Field(..., description="Identifier for the submission.")
    status: str = Field(..., description="Status of the submission.")
    feedback: List[FeedbackBlock] = Field(default_factory=list)
