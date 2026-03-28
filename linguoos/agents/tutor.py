from __future__ import annotations

from typing import Any

from linguoos.agents.base import BaseAgent


class TutorAgent(BaseAgent):
    async def respond(self, message: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        context = context or {}
        reply = await self.provider.chat_tutor(message=message, context=context)
        return {
            "reply": reply,
        }
