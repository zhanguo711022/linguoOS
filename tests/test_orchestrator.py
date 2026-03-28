import os

os.environ["LINGUO_DB_PATH"] = "/tmp/linguoos_test.db"

from linguoos.core.domain import LearningRecord
from linguoos.core.orchestrator import OrchestratorV2


def test_orchestrator_first_step():
    decision = OrchestratorV2().decide([], {})
    assert decision.action == "practice"
    assert decision.reason == "first_step"


def test_orchestrator_wrong_streak():
    records = [
        LearningRecord(session_id="s", action_type="practice", payload={}, correct=False),
        LearningRecord(session_id="s", action_type="practice", payload={}, correct=False),
        LearningRecord(session_id="s", action_type="practice", payload={}, correct=False),
    ]
    decision = OrchestratorV2().decide(records, {})
    assert decision.action == "explain"


def test_orchestrator_correct_streak():
    records = [
        LearningRecord(session_id="s", action_type="practice", payload={}, correct=True),
        LearningRecord(session_id="s", action_type="practice", payload={}, correct=True),
        LearningRecord(session_id="s", action_type="practice", payload={}, correct=True),
    ]
    decision = OrchestratorV2().decide(records, {})
    assert decision.action in {"review", "complete"}
