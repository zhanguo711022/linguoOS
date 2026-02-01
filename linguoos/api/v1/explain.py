from fastapi import APIRouter, Query

from linguoos.schemas.explain import Explanation

router = APIRouter(prefix="/api/v1/explain", tags=["explain"])


@router.get("/concept", response_model=Explanation)
def concept(module_id: str = Query("precision.generalization")) -> Explanation:
    if module_id == "precision.vague_modifiers":
        return Explanation(
            title="Vague Modifiers",
            one_liner="Prefer measurable modifiers over vague adverbs/adjectives.",
            structure_template=["Target", "Measure", "Time frame"],
            example="Average scores increased by 12% over 4 weeks.",
        )
    return Explanation(
        title="Generalization",
        one_liner="SAT favors specific, verifiable claims over broad generalizations.",
        structure_template=["Scope", "Object", "Measurable evidence"],
        example="In Grade 10, average scores rose 12% after a 4-week program.",
    )
