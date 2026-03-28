from __future__ import annotations

from typing import Protocol

from linguoos.storage.base import Repository


class NotificationChannel(Protocol):
    async def notify(self, teacher_id: str, message: str, context: dict) -> bool: ...


class InterventionService:
    def __init__(self, repo: Repository, channels: dict[str, NotificationChannel] | None = None) -> None:
        self._repo = repo
        self._channels = channels or {}

    async def flag_for_intervention(self, session_id: str, reason: str, context: dict) -> int:
        return await self._repo.create_intervention(session_id, reason, context)

    async def list_pending(self) -> list[dict]:
        return await self._repo.list_interventions(status="pending")

    async def resolve(self, intervention_id: int, teacher_response: str) -> None:
        await self._repo.resolve_intervention(intervention_id, teacher_response)
