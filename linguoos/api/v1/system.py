import time

from fastapi import APIRouter, Query
from pydantic import BaseModel

from linguoos import config
from linguoos.system.events import EVENTS
from linguoos.system.metrics import METRICS

router = APIRouter(prefix="/api/v1/system", tags=["system"])
STARTED_AT = time.time()


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


@router.get("/status")
def status() -> dict:
    uptime_sec = int(time.time() - STARTED_AT)
    return {
        "ok": True,
        "version": config.VERSION,
        "uptime_sec": uptime_sec,
        "require_api_key": config.REQUIRE_API_KEY,
    }


@router.get("/metrics")
def metrics() -> dict:
    return METRICS.snapshot()


@router.get("/events")
def events(limit: int | None = Query(None, ge=1, le=500)) -> dict:
    return {
        "events": EVENTS.list(limit=limit),
        "meta": EVENTS.snapshot(),
    }
