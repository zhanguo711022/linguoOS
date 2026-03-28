from __future__ import annotations

import uuid
from datetime import datetime

from linguoos.agents.tutor import TutorAgent
from linguoos.core.domain import LearningRecord, Session
from linguoos.core.orchestrator import OrchestratorV2
from linguoos.storage.base import Repository


class SessionService:
    def __init__(self, repo: Repository, tutor: TutorAgent, orchestrator: OrchestratorV2) -> None:
        self._repo = repo
        self._tutor = tutor
        self._orchestrator = orchestrator

    async def start(self, user_id: str, language: str | None = None) -> dict:
        session_id = uuid.uuid4().hex
        session = Session(session_id=session_id, user_id=user_id, language=language)
        await self._repo.create_session(session)
        decision = self._orchestrator.decide([], {})
        welcome = "Welcome to LinguoOS. Let's begin your first activity."
        await self._repo.add_record(
            LearningRecord(
                session_id=session_id,
                action_type="session_start",
                payload={"welcome": welcome, "decision": decision.action},
                correct=None,
            )
        )
        return {
            "session_id": session_id,
            "welcome_message": welcome,
            "first_action": decision.action,
        }

    async def handle_message(self, session_id: str, message: str) -> dict:
        session = await self._repo.get_session(session_id)
        if not session:
            raise ValueError("Session not found")
        history = await self._repo.list_records(session_id=session_id, limit=20)
        reply = await self._tutor.respond(message=message, context={"session_id": session_id})
        await self._repo.add_record(
            LearningRecord(
                session_id=session_id,
                action_type="message",
                payload={"message": message, "reply": reply["reply"]},
                correct=None,
            )
        )
        decision = self._orchestrator.decide(history, {})
        return {
            "reply": reply["reply"],
            "next_action": decision.action,
            "intervention_flagged": False,
        }

    async def history(self, session_id: str) -> list[LearningRecord]:
        return await self._repo.list_records(session_id=session_id, limit=50)

    async def end(self, session_id: str) -> None:
        await self._repo.update_session_status(session_id, status="complete")
        await self._repo.add_record(
            LearningRecord(
                session_id=session_id,
                action_type="session_end",
                payload={"ended_at": datetime.utcnow().isoformat()},
                correct=None,
            )
        )
