from fastapi import APIRouter

router = APIRouter(prefix="/correction", tags=["correction"])


@router.post("/review")
async def correction_review(payload: dict):
    return {"ok": True, "data": {"received": payload}}
