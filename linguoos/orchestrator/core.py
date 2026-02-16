from linguoos.schemas.decision import Action, OrchestratorDecision


class Orchestrator:
    def decide_next_action(self, profile, workspace_state, decision_input):
        """Decide next action using lightweight, deterministic rules.

        v1.1 reason rules:
        - first request -> practice / "first step"
        - after practice + correct -> practice / "keep momentum"
        - after practice + wrong -> explain / "after wrong answer"
        """
        # First turn
        if decision_input.last_mode is None:
            return OrchestratorDecision(
                action=Action.practice,
                target_module=decision_input.module_id,
                reason="first step",
            )

        # After practice
        if decision_input.last_mode == "practice":
            if decision_input.last_correct is False:
                return OrchestratorDecision(
                    action=Action.explain,
                    target_module=decision_input.module_id,
                    reason="after wrong answer",
                )
            if decision_input.last_correct is True:
                return OrchestratorDecision(
                    action=Action.practice,
                    target_module=decision_input.module_id,
                    reason="keep momentum",
                )

        # Fallback: keep moving in practice.
        return OrchestratorDecision(
            action=Action.practice,
            target_module=decision_input.module_id,
            reason="keep momentum",
        )

    def route_to_agent(self, action):
        """Return a placeholder agent name without instantiating models."""
        return "practice"
