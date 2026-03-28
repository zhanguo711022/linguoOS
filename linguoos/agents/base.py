from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from linguoos.providers.base import LLMProvider


class Agent(Protocol):
    provider: LLMProvider


@dataclass
class BaseAgent:
    provider: LLMProvider
