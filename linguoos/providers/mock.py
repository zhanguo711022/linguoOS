from __future__ import annotations

from typing import Any, Dict


class MockProvider:
    name = "mock"

    def explain(self, module_id: str) -> Dict[str, Any]:
        return {
            "module_id": module_id,
            "title": f"Mock explanation for {module_id}",
            "content": "This is a mock provider response. Replace via providers/ when enabling real LLMs.",
        }

    def evaluate_precision(self, text: str) -> Dict[str, Any]:
        # Deterministic placeholder signal; callers must not rely on semantics.
        ok = len(text.strip()) > 10
        return {
            "ok": ok,
            "score": 0.6 if ok else 0.2,
            "notes": "mock evaluation",
        }
