from linguoos.schemas.explain import Explanation


class ExplainAgent:
    def explain(self, module_id: str) -> Explanation:
        if module_id == "precision.vague_modifiers":
            return Explanation(
                title="Vague Modifiers",
                one_liner="Prefer measurable modifiers over vague adverbs/adjectives.",
                structure_template=["Target", "Measure", "Time frame"],
                example="Average scores increased by 12% over 4 weeks.",
                return_to="practice"
            )
        return Explanation(
            title="Generalization",
            one_liner="Favor specific, verifiable claims over broad generalizations.",
            structure_template=["Scope", "Object", "Measurable evidence"],
            example="In Grade 10, average scores rose 12% after a 4‑week program.",
            return_to="practice"
        )
