from fastapi import APIRouter

from linguoos.content.precision_registry import MODULES

router = APIRouter(prefix="/precision", tags=["precision"])


@router.get("/modules")
async def precision_modules():
    return {"ok": True, "data": [module.model_dump() for module in MODULES]}
