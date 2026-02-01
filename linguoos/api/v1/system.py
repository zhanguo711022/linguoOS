from fastapi import APIRouter
from pydantic import BaseModel

from linguoos import config

router = APIRouter(prefix="/api/v1/system", tags=["system"])


class Health(BaseModel):
    ok: bool


class Version(BaseModel):
    version: str


@router.get("/health", response_model=Health)
def health() -> Health:
    return Health(ok=True)


@router.get("/version", response_model=Version)
def version() -> Version:
    return Version(version=config.VERSION)
