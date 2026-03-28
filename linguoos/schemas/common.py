from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel


class ErrorDetail(BaseModel):
    type: str
    message: str | None = None
    details: dict | None = None


T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    ok: bool = True
    data: T | None = None
    error: ErrorDetail | None = None
