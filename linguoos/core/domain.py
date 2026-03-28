from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class Student:
    user_id: str
    language: str | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Course:
    course_id: str
    title: str
    modules: list[str] = field(default_factory=list)


@dataclass
class Session:
    session_id: str
    user_id: str
    language: str | None = None
    status: str = "active"
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class LearningRecord:
    session_id: str
    action_type: str
    payload: dict[str, Any]
    correct: bool | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)
