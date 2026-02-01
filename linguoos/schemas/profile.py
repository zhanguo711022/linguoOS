from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Dict

from pydantic import BaseModel, Field


class AbilityName(str, Enum):
    precision = "precision"
    structure = "structure"
    logic = "logic"
    usage = "usage"
    sound = "sound"


class AbilityDimension(BaseModel):
    level: int = Field(..., ge=0, le=100)
    trend: str | None = None
    last_updated: datetime


class LanguageProfile(BaseModel):
    user_id: str
    language: str
    current_stage: int = Field(..., ge=0, le=4)
    ability_dimensions: Dict[AbilityName, AbilityDimension]


class LanguageProfileUpdate(BaseModel):
    user_id: str | None = None
    language: str | None = None
    current_stage: int | None = Field(default=None, ge=0, le=4)
    ability_dimensions: Dict[AbilityName, AbilityDimension] | None = None
