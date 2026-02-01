from fastapi import APIRouter, Query

from linguoos.schemas.state import GrowthOverview

router = APIRouter(prefix="/api/v1/growth", tags=["growth"])


@router.get("/overview", response_model=GrowthOverview)
def get_growth_overview(user_id: str = Query(...)) -> GrowthOverview:
    return GrowthOverview(
        user_id=user_id,
        milestones=["mock-milestone-1", "mock-milestone-2"],
        summary="Mock growth overview placeholder.",
    )
