import os
import pytest

os.environ["LINGUO_DB_PATH"] = "/tmp/linguoos_test.db"

from linguoos.agents.assessor import AssessorAgent
from linguoos.agents.explainer import ExplainerAgent
from linguoos.agents.tutor import TutorAgent
from linguoos.core.orchestrator import OrchestratorV2
from linguoos.config import settings
from linguoos.providers.mock import MockProvider
from linguoos.services.explain_service import ExplainService
from linguoos.services.practice_service import PracticeService
from linguoos.services.session_service import SessionService
from linguoos.storage.sqlite import SQLiteRepository


@pytest.mark.asyncio
async def test_services_flow(tmp_path):
    settings.db_path = str(tmp_path / "history.db")
    repo = SQLiteRepository()
    await repo.init()
    provider = MockProvider()

    session_service = SessionService(repo, TutorAgent(provider), OrchestratorV2())
    practice_service = PracticeService(repo, provider, AssessorAgent(provider))
    explain_service = ExplainService(repo, ExplainerAgent(provider))

    start = await session_service.start(user_id="u1", language="en")
    session_id = start["session_id"]

    item = await practice_service.next_item(session_id=session_id, module_id="grammar")
    result = await practice_service.submit(
        session_id=session_id,
        prompt=item["prompt"],
        answer=item["expected_answer"],
        expected_answer=item["expected_answer"],
    )
    assert "feedback" in result

    explanation = await explain_service.explain(session_id=session_id, concept="past tense")
    assert explanation["concept"] == "past tense"
