from __future__ import annotations

from fastapi import APIRouter, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from linguoos.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


class RegisterRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


def _get_auth_service() -> AuthService:
    return AuthService()


def _extract_bearer_token(authorization: str | None) -> str | None:
    if not authorization:
        return None
    if not authorization.startswith("Bearer "):
        return None
    return authorization.split(" ", 1)[1].strip() or None


@router.post("/register")
async def register(payload: RegisterRequest):
    service = _get_auth_service()
    try:
        user_id = service.register(payload.email, payload.password)
    except ValueError as exc:
        return JSONResponse(
            {"ok": False, "error": {"type": "auth", "message": str(exc)}},
            status_code=400,
        )
    return {"ok": True, "data": {"user_id": user_id}}


@router.post("/login")
async def login(payload: LoginRequest):
    service = _get_auth_service()
    try:
        token = service.login(payload.email, payload.password)
    except ValueError as exc:
        return JSONResponse(
            {"ok": False, "error": {"type": "auth", "message": str(exc)}},
            status_code=401,
        )
    except RuntimeError as exc:
        return JSONResponse(
            {"ok": False, "error": {"type": "config", "message": str(exc)}},
            status_code=500,
        )
    return {"ok": True, "data": {"token": token}}


@router.get("/me")
async def me(authorization: str | None = Header(default=None)):
    token = _extract_bearer_token(authorization)
    if not token:
        return JSONResponse(
            {"ok": False, "error": {"type": "auth", "message": "missing bearer token"}},
            status_code=401,
        )
    service = _get_auth_service()
    try:
        user_id = service.verify_token(token)
    except ValueError as exc:
        return JSONResponse(
            {"ok": False, "error": {"type": "auth", "message": str(exc)}},
            status_code=401,
        )
    except RuntimeError as exc:
        return JSONResponse(
            {"ok": False, "error": {"type": "config", "message": str(exc)}},
            status_code=500,
        )
    return {"ok": True, "data": {"user_id": user_id}}
