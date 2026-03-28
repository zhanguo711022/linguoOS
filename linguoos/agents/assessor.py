from __future__ import annotations

from typing import Any

from linguoos.agents.base import BaseAgent


class AssessorAgent(BaseAgent):
    async def assess(self, prompt: str, answer: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        context = context or {}
        return await self.provider.assess_practice(prompt=prompt, answer=answer, context=context)
