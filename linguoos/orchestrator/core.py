from linguoos.schemas.decision import Action, OrchestratorDecision


class Orchestrator:
    def decide_next_action(self, profile, workspace_state, decision_input):
        """Return a placeholder action payload without business logic."""
        if decision_input.last_mode == "practice" and decision_input.last_correct is False:
            return OrchestratorDecision(
                action=Action.explain,
                target_module=decision_input.module_id,
                reason="placeholder",
            )
        return OrchestratorDecision(
            action=Action.practice,
            target_module=decision_input.module_id,
            reason="placeholder",
        )

    def route_to_agent(self, action):
        """Return a placeholder agent name without instantiating models."""
        return "practice"
