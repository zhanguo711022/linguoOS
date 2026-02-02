import re

from linguoos.schemas.task import TaskSubmissionRequest
from linguoos.schemas.feedback import FeedbackResponse, FeedbackBlock


class FeedbackAgent:
    def evaluate(self, req: TaskSubmissionRequest) -> FeedbackResponse:
        text = ""
        try:
            text = (req.payload or {}).get("content", "")
        except Exception:
            text = ""
        has_number = bool(re.search(r"\d", text))
        if has_number:
            return FeedbackResponse(
                mode="feedback",
                core_issue="precision",
                blocks=[
                    FeedbackBlock(
                        type="why",
                        content="Includes measurable evidence (numbers/time).",
                    ),
                    FeedbackBlock(
                        type="example",
                        content="Average scores increased by 12% after 4 weeks.",
                    ),
                    FeedbackBlock(
                        type="how_to_avoid",
                        content="Prefer measurable claims to vague statements.",
                    ),
                ],
                next_action="continue_practice",
            )
        return FeedbackResponse(
            mode="feedback",
            core_issue="precision",
            blocks=[
                FeedbackBlock(type="error_type", content="generalization"),
                FeedbackBlock(
                    type="why",
                    content="The claim is broad and not verifiable.",
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
