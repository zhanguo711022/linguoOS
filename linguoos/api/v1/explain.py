from fastapi import APIRouter, Query

from linguoos.agents.explain import ExplainAgent
from linguoos.schemas.explain import Explanation

router = APIRouter(prefix="/api/v1/explain", tags=["explain"])


@router.get("/concept", response_model=Explanation)
def concept(module_id: str = Query("precision.generalization")) -> Explanation:
    return ExplainAgent().explain(module_id)
