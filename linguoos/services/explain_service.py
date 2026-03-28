from __future__ import annotations

from linguoos.agents.explainer import ExplainerAgent
from linguoos.core.domain import LearningRecord
from linguoos.storage.base import Repository


class ExplainService:
    def __init__(self, repo: Repository, explainer: ExplainerAgent) -> None:
        self._repo = repo
        self._explainer = explainer

    async def explain(self, session_id: str, concept: str, level: str | None = None) -> dict:
        explanation = await self._explainer.explain(concept=concept, level=level)
        await self._repo.add_record(
            LearningRecord(
                session_id=session_id,
                action_type="explain",
                payload=explanation,
                correct=None,
            )
        )
        return explanation
