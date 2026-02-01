from typing import List

from fastapi import APIRouter

from linguoos.content.precision_registry import MODULES
from linguoos.schemas.precision import PrecisionModule

router = APIRouter(prefix="/api/v1/precision", tags=["precision"])


@router.get("/modules", response_model=List[PrecisionModule])
def list_modules() -> List[PrecisionModule]:
    return MODULES
