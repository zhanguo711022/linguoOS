from __future__ import annotations

from typing import Any

from linguoos.agents.base import BaseAgent


class ExplainerAgent(BaseAgent):
    async def explain(self, concept: str, level: str | None = None, context: dict[str, Any] | None = None) -> dict[str, Any]:
        context = context or {}
        return await self.provider.explain_concept(concept=concept, level=level, context=context)
