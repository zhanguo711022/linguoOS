from typing import Any, Dict, List

from fastapi import APIRouter, Query
from pydantic import BaseModel

from linguoos.api.v1.explain import concept as explain_concept
from linguoos.api.v1.practice import next_practice
from linguoos.api.v1.practice import submit as practice_submit
from linguoos.orchestrator.core import Orchestrator
from linguoos.schemas.decision import DecisionInput
from linguoos.schemas.task import TaskSubmissionRequest

router = APIRouter(prefix="/api/v1/demo", tags=["demo"])


class Step(BaseModel):
    name: str
    data: Dict[str, Any]


class DemoResult(BaseModel):
    steps: List[Step]


@router.get("/flow", response_model=DemoResult)
def flow(
    module_id: str = Query("precision.generalization"),
    wrong_first: bool = Query(True),
) -> DemoResult:
    steps: List[Step] = []
    orch = Orchestrator()

    d1 = orch.decide_next_action(
        profile=None,
        workspace_state=None,
        decision_input=DecisionInput(
            user_id="demo",
            module_id=module_id,
            last_mode=None,
            last_correct=None,
        ),
    )
    steps.append(Step(name="decision_1", data=d1.model_dump()))

    item = next_practice(module_id=module_id)
    steps.append(Step(name="practice_next", data=item.model_dump()))

    wrong_content = "Students often learn much faster."
    right_content = "Average scores increased by 12% after 4 weeks."
    chosen = wrong_content if wrong_first else right_content

    req = TaskSubmissionRequest(
        user_id="demo",
        input_type="text",
        payload={"content": chosen},
        client_context={
            "client_type": "demo",
            "workspace_mode": "practice",
            "timestamp": 1730000000,
        },
    )
    fb = practice_submit(req)
    steps.append(Step(name="practice_submit", data=fb.model_dump()))

    d2 = orch.decide_next_action(
        profile=None,
        workspace_state=None,
        decision_input=DecisionInput(
            user_id="demo",
            module_id=module_id,
            last_mode="practice",
            last_correct=(not wrong_first),
        ),
    )
    steps.append(Step(name="decision_2", data=d2.model_dump()))

    if d2.action.value == "explain":
        exp = explain_concept(module_id=module_id)
        steps.append(Step(name="explain_concept", data=exp.model_dump()))

    return DemoResult(steps=steps)
