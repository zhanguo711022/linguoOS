class Orchestrator:
    def decide_next_action(self, profile, workspace_state):
        """Return a placeholder action payload without business logic."""
        return {"action": "practice", "reason": "placeholder"}

    def route_to_agent(self, action):
        """Return a placeholder agent name without instantiating models."""
        return "practice"
