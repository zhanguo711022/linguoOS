from unittest import TestCase
from unittest.mock import patch

from linguoos.api.v1.explain import concept
from linguoos.api.v1.practice import next_practice, submit
from linguoos.schemas.explain import Explanation
from linguoos.schemas.feedback import FeedbackBlock, FeedbackResponse
from linguoos.schemas.practice import PracticeItem
from linguoos.schemas.task import TaskSubmissionRequest


class AgentsWiringTests(TestCase):
    def test_practice_next_uses_practice_agent(self):
        fake_item = PracticeItem(
            task_id="t-1",
            module_id="precision.generalization",
            type="choice",
            prompt="p",
            options=["a", "b"],
        )
        with patch("linguoos.api.v1.practice.PracticeAgent.generate_item", return_value=fake_item) as m:
            out = next_practice("precision.generalization")
            m.assert_called_once_with("precision.generalization")
            self.assertEqual(out.task_id, "t-1")

    def test_practice_submit_uses_feedback_agent(self):
        req = TaskSubmissionRequest(
            user_id="u1",
            input_type="text",
            payload={"content": "Average rose 12%"},
            client_context={"client_type": "test"},
        )
        fake = FeedbackResponse(
            mode="feedback",
            core_issue="precision",
            blocks=[FeedbackBlock(type="why", content="ok")],
            next_action="continue_practice",
        )
        with patch("linguoos.api.v1.practice.FeedbackAgent.evaluate", return_value=fake) as m_eval, patch(
            "linguoos.api.v1.practice.save_attempt", return_value=None
        ) as m_save:
            out = submit(req)
            m_eval.assert_called_once()
            m_save.assert_called_once()
            self.assertEqual(out.mode, "feedback")

    def test_explain_concept_uses_explain_agent(self):
        with patch("linguoos.api.v1.explain.ExplainAgent.explain") as m:
            m.return_value = Explanation(
                title="Generalization",
                one_liner="x",
                structure_template=["a", "b", "c"],
                example="e",
                return_to="practice",
            )
            out = concept("precision.generalization")
            m.assert_called_once_with("precision.generalization")
            self.assertEqual(out.title, "Generalization")
