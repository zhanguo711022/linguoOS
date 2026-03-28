from __future__ import annotations

from enum import Enum

from pydantic import BaseModel


class ErrorType(str, Enum):
    generalization = "generalization"
    unverifiable = "unverifiable"
    scope_mismatch = "scope_mismatch"
    causal_overreach = "causal_overreach"
    vague_modifiers = "vague_modifiers"


class PrecisionModule(BaseModel):
    module_id: str
    name: str
    description: str
    error_type: ErrorType
