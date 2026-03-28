from __future__ import annotations

from typing import Dict, List

from pydantic import BaseModel


class LevelInfo(BaseModel):
    id: str
    name: str
    name_zh: str
    cefr: str
    desc: str
    emoji: str
    color: str
    target: str


class ModuleInfo(BaseModel):
    id: str
    name: str
    name_zh: str
    desc: str
    level_id: str
    order: int
    emoji: str


class Question(BaseModel):
    id: str
    type: str
    level: str
    prompt: str
    options: List[str]
    answer: str
    explanation: str


class ExplainContent(BaseModel):
    title: str
    one_liner: str
    steps: List[str]
    example: str
    tip: str


class ProgressUpdate(BaseModel):
    user_id: str
    level_id: str
    module_id: str
    completed: bool
    score: float


class UserProgress(BaseModel):
    user_id: str
    level_id: str
    modules: Dict[str, float]
