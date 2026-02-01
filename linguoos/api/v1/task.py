from uuid import uuid4

from fastapi import APIRouter

from linguoos.schemas.feedback import FeedbackBlock, FeedbackResponse
from linguoos.schemas.task import TaskSubmissionRequest

router = APIRouter(prefix="/api/v1/task", tags=["task"])


@router.post("/submit", response_model=FeedbackResponse)
def submit_task(request: TaskSubmissionRequest) -> FeedbackResponse:
    return FeedbackResponse(
        submission_id=str(uuid4()),
        status="received",
        feedback=[
            FeedbackBlock(
                block_id="mock-feedback-1",
                message="Mock feedback placeholder.",
                metadata={"user_id": request.user_id, "task_id": request.task_id},
            )
        ],
    )
