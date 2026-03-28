from __future__ import annotations

from pydantic import BaseModel


class ProfileCore(BaseModel):
    grammar: float = 0.5
    vocabulary: float = 0.5
    fluency: float = 0.5
    comprehension: float = 0.5
    confidence: float = 0.5
