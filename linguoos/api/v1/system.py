from fastapi import APIRouter

from linguoos.config import settings
from linguoos.system.events import EVENTS
from linguoos.system.metrics import METRICS

router = APIRouter(prefix="/system", tags=["system"])


@router.get("/health")
async def health():
    return {"ok": True, "data": {"status": "ok"}}


@router.get("/version")
async def version():
    return {"ok": True, "data": {"version": settings.version}}


@router.get("/status")
async def status():
    return {"ok": True, "data": {"provider": settings.provider, "debug": settings.debug}}


@router.get("/metrics")
async def metrics():
    return {"ok": True, "data": METRICS.snapshot()}


@router.get("/events")
async def events(limit: int | None = None):
    return {"ok": True, "data": EVENTS.list(limit=limit)}
