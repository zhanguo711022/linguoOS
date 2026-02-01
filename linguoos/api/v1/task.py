from fastapi import APIRouter

from linguoos.schemas.feedback import FeedbackBlock, FeedbackResponse
from linguoos.schemas.task import TaskSubmissionRequest

router = APIRouter(prefix="/api/v1/task", tags=["task"])


@router.post("/submit", response_model=FeedbackResponse)
def submit_task(request: TaskSubmissionRequest) -> FeedbackResponse:
    return FeedbackResponse(
        mode="feedback",
        core_issue="precision",
        blocks=[
            FeedbackBlock(
                type="info",
                content=(
                    "Mock feedback placeholder for task "
                    f"{request.task_id} submitted by {request.user_id}."
                ),
            )
        ],
        next_action="continue_practice",
    )
