from __future__ import annotations

from linguoos.agents.assessor import AssessorAgent
from linguoos.core.domain import LearningRecord
from linguoos.storage.base import Repository
from linguoos.providers.base import LLMProvider


class PracticeService:
    def __init__(self, repo: Repository, provider: LLMProvider, assessor: AssessorAgent) -> None:
        self._repo = repo
        self._provider = provider
        self._assessor = assessor

    async def next_item(self, session_id: str, module_id: str) -> dict:
        item = await self._provider.generate_practice(module_id=module_id)
        await self._repo.add_record(
            LearningRecord(
                session_id=session_id,
                action_type="practice_item",
                payload=item,
                correct=None,
            )
        )
        return item

    async def submit(self, session_id: str, prompt: str, answer: str, expected_answer: str | None = None) -> dict:
        result = await self._assessor.assess(
            prompt=prompt,
            answer=answer,
            context={"expected_answer": expected_answer},
        )
        await self._repo.add_record(
            LearningRecord(
                session_id=session_id,
                action_type="practice_submit",
                payload={"prompt": prompt, "answer": answer, "feedback": result},
                correct=bool(result.get("correct")),
            )
        )
        return result
