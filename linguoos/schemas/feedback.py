from typing import List

from pydantic import BaseModel, Field


class FeedbackBlock(BaseModel):
    type: str
    content: str


class FeedbackResponse(BaseModel):
    mode: str
    core_issue: str
    blocks: List[FeedbackBlock] = Field(default_factory=list)
    next_action: str
