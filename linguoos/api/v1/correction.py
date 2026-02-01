from fastapi import APIRouter
from pydantic import BaseModel

from linguoos.schemas.feedback import FeedbackBlock, FeedbackResponse

router = APIRouter(prefix="/api/v1/correction", tags=["correction"])


class CorrectionRequest(BaseModel):
    text: str
    module_id: str = "precision.generalization"


@router.post("/review", response_model=FeedbackResponse)
def review(req: CorrectionRequest) -> FeedbackResponse:
    return FeedbackResponse(
        mode="feedback",
        core_issue="precision",
        blocks=[
            FeedbackBlock(type="error_type", content="generalization"),
            FeedbackBlock(
                type="why", content="The claim is broad and not verifiable."
            ),
            FeedbackBlock(
                type="example",
                content="Average scores increased by 12% after 4 weeks.",
            ),
            FeedbackBlock(
                type="how_to_avoid",
                content="Constrain scope and use measurable evidence.",
            ),
        ],
        next_action="continue_practice",
    )
