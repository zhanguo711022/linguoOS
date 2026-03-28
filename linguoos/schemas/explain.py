from __future__ import annotations

from pydantic import BaseModel


class Explanation(BaseModel):
    concept: str
    level: str
    structure_template: dict
    example: str
