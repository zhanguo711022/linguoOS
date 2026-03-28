from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from linguoos.core.domain import LearningRecord


@dataclass
class OrchestratorDecision:
    action: str
    reason: str
    confidence: float


class OrchestratorV2:
    def decide(self, history: Iterable[LearningRecord], error_stats: dict | None = None) -> OrchestratorDecision:
        records = list(history)
        if not records:
            return OrchestratorDecision(action="practice", reason="first_step", confidence=0.75)

        correct_streak = 0
        wrong_streak = 0
        for record in reversed(records):
            if record.correct is None:
                break
            if record.correct:
                if wrong_streak:
                    break
                correct_streak += 1
            else:
                if correct_streak:
                    break
                wrong_streak += 1

        if wrong_streak >= 3:
            return OrchestratorDecision(action="explain", reason="after_wrong", confidence=0.82)

        if correct_streak >= 3:
            action = "review" if correct_streak == 3 else "complete"
            reason = "keep_momentum" if action == "review" else "goal_reached"
            return OrchestratorDecision(action=action, reason=reason, confidence=0.86)

        if error_stats and error_stats.get("needs_review"):
            return OrchestratorDecision(action="review", reason="needs_review", confidence=0.7)

        return OrchestratorDecision(action="practice", reason="keep_momentum", confidence=0.65)
