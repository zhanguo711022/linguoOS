from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class ErrorType(str, Enum):
    generalization = "generalization"
    unverifiable = "unverifiable"
    scope_mismatch = "scope_mismatch"
    causal_overreach = "causal_overreach"
    vague_modifiers = "vague_modifiers"


class PrecisionModule(BaseModel):
    module_id: str = Field(..., description='Example: "precision.generalization"')
    name: str = Field(..., description="Example: Generalization")
    description: str
    error_type: ErrorType
    prerequisites: List[str] = []
    mastery_condition: Dict[str, Optional[str]] = {}
