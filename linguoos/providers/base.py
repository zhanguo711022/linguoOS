from typing import Protocol, Dict, Any


class LLMProvider(Protocol):
    name: str

    def explain(self, module_id: str) -> Dict[str, Any]:
        ...

    def evaluate_precision(self, text: str) -> Dict[str, Any]:
        ...
