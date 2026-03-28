from __future__ import annotations

import random
from datetime import datetime
from typing import Any


class MockProvider:
    def __init__(self) -> None:
        self._questions = {
            "grammar": [
                ("Choose the correct form: 'She ___ to school every day.'", "goes"),
                ("Fill the blank: 'They have ___ their homework.'", "finished"),
                ("Rewrite: 'He can swim.' in past ability.", "He could swim."),
                ("Pick the correct article: '___ apple a day keeps the doctor away.'", "An"),
                ("Convert to passive: 'The chef cooks the meal.'", "The meal is cooked by the chef."),
            ],
            "vocabulary": [
                ("Give a synonym for 'rapid'.", "quick"),
                ("What is the opposite of 'scarce'?", "abundant"),
                ("Use 'meticulous' in a sentence.", "She is meticulous with her notes."),
                ("Define 'sustainable' in one sentence.", "Able to be maintained without harming resources."),
                ("Pick the best word: 'The plan is ___.' (feasible/fragile)", "feasible"),
            ],
            "listening": [
                ("Imagine you hear: 'I'll be there in a sec.' What does it mean?", "in a moment"),
                ("If someone says 'Could you speak up?' what do they want?", "to speak louder"),
                ("You hear 'Let's call it a day.' What does it imply?", "stop working"),
                ("Interpret: 'I'm tied up right now.'", "busy"),
                ("You hear 'Touch base tomorrow.' What's the plan?", "follow up tomorrow"),
            ],
        }

    async def chat_tutor(self, message: str, context: dict[str, Any]) -> str:
        module_hint = context.get("module_id", "general")
        return (
            f"Got it. Let's focus on {module_hint}. "
            "Tell me one thing you want to improve, and I'll tailor the next practice."
        )

    async def generate_practice(self, module_id: str, difficulty: str | None = None) -> dict[str, Any]:
        module_questions = self._questions.get(module_id, [])
        if not module_questions:
            module_questions = sum(self._questions.values(), [])
        prompt, expected = random.choice(module_questions)
        return {
            "id": f"mock-{random.randint(1000, 9999)}",
            "module_id": module_id,
            "prompt": prompt,
            "expected_answer": expected,
            "difficulty": difficulty or "core",
            "created_at": datetime.utcnow().isoformat(),
        }

    async def assess_practice(self, prompt: str, answer: str, context: dict[str, Any]) -> dict[str, Any]:
        expected = context.get("expected_answer", "")
        normalized = answer.strip().lower()
        expected_norm = str(expected).strip().lower()
        is_correct = expected_norm and expected_norm in normalized
        if not expected_norm:
            is_correct = bool(normalized)
        return {
            "correct": is_correct,
            "score": 1.0 if is_correct else 0.4,
            "feedback": {
                "why": "Your answer matches the key idea." if is_correct else "The response misses the target phrase.",
                "example": expected or "" ,
                "how_to_avoid": "Focus on tense and key vocabulary for this module.",
            },
        }

    async def explain_concept(self, concept: str, level: str | None, context: dict[str, Any]) -> dict[str, Any]:
        return {
            "concept": concept,
            "level": level or "core",
            "structure_template": {
                "overview": f"{concept} helps you express meaning clearly.",
                "steps": [
                    "State the core definition.",
                    "Show 2 common patterns.",
                    "Give 1 real-world example.",
                    "Invite a short practice response.",
                ],
            },
            "example": f"Example: I used {concept} to describe a past habit.",
        }
