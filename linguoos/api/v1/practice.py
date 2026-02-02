from fastapi import APIRouter, Query

from linguoos.agents.feedback import FeedbackAgent
from linguoos.schemas.feedback import FeedbackResponse
from linguoos.schemas.practice import PracticeItem
from linguoos.schemas.task import TaskSubmissionRequest

router = APIRouter(prefix="/api/v1/practice", tags=["practice"])


@router.get("/next", response_model=PracticeItem)
def next_practice(
    module_id: str = Query("precision.generalization"),
) -> PracticeItem:
    return PracticeItem(
        task_id="demo-1",
        module_id=module_id,
        type="choice",
        prompt="Which option is the most precise?",
        options=[
            "Students often learn much faster.",
            "Average scores increased by 12% after 4 weeks.",
        ],
    )


@router.post("/submit", response_model=FeedbackResponse)
def submit(req: TaskSubmissionRequest) -> FeedbackResponse:
    return FeedbackAgent().evaluate(req)
