from fastapi import APIRouter, Query

from linguoos.agents.feedback import FeedbackAgent
from linguoos.agents.practice import PracticeAgent
from linguoos.schemas.feedback import FeedbackResponse
from linguoos.schemas.practice import PracticeItem
from linguoos.schemas.task import TaskSubmissionRequest
from linguoos.storage.sqlite import save_attempt

router = APIRouter(prefix="/api/v1/practice", tags=["practice"])


@router.get("/next", response_model=PracticeItem)
def next_practice(
    module_id: str = Query("precision.generalization"),
) -> PracticeItem:
    return PracticeAgent().generate_item(module_id)


@router.post("/submit", response_model=FeedbackResponse)
def submit(req: TaskSubmissionRequest) -> FeedbackResponse:
    result = FeedbackAgent().evaluate(req)
    text = (req.payload or {}).get("content", "")
    module_id = (req.payload or {}).get("module_id") or "precision.generalization"
    correct = False
    save_attempt(req.user_id, module_id, text, correct)
    return result
