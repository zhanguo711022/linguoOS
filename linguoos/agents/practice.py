from typing import Optional, List, Literal

from linguoos.schemas.practice import PracticeItem


class PracticeAgent:
    def generate_item(self, module_id: str = "precision.generalization") -> PracticeItem:
        return PracticeItem(
            task_id="demo-1",
            module_id=module_id,
            type="choice",
            prompt="Which option is the most precise?",
            options=[
                "Students often learn much faster.",
                "Average scores increased by 12% after 4 weeks."
            ]
        )
