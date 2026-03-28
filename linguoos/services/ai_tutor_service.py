from __future__ import annotations

import json
from typing import Any

from openai import AsyncOpenAI

from linguoos.config import settings


class AITutorService:
    def __init__(self, client: AsyncOpenAI | None = None) -> None:
        self._client = client or AsyncOpenAI(api_key=settings.openai_api_key)

    def _is_mock(self) -> bool:
        return not settings.openai_api_key

    def _fallback_explanation(self, language: str) -> dict[str, Any]:
        return {
            "explanation": "EN: Let's review the key idea step by step. ZH: 我们一步步复习关键点。",
            "correct_pattern": "EN: Use a clear structure and natural phrasing. ZH: 结构清晰、用语自然。",
            "encouragement": "EN: You're close—keep going! ZH: 已经很接近了，加油！",
            "follow_up_question": "",
            "follow_up_options": [],
            "follow_up_answer": "",
        }

    def _normalize(self, payload: dict[str, Any], fallback: dict[str, Any]) -> dict[str, Any]:
        normalized = fallback.copy()
        for key in normalized:
            if key in payload and payload[key] is not None:
                normalized[key] = payload[key]
        if not isinstance(normalized.get("follow_up_options"), list):
            normalized["follow_up_options"] = []
        return normalized

    async def explain_wrong_answer(
        self,
        question: str,
        wrong_answer: str,
        correct_answer: str,
        module_id: str,
        language: str,
    ) -> dict[str, Any]:
        fallback = self._fallback_explanation(language)
        if self._is_mock():
            return fallback

        system_prompt = (
            "You are a friendly language teacher. Keep explanations short, kind, and practical. "
            "Always provide bilingual output (English + Chinese). "
            "Return a JSON object with keys: explanation, correct_pattern, encouragement, "
            "follow_up_question, follow_up_options, follow_up_answer. "
            "If no follow-up is needed, use empty string and empty list."
        )
        user_prompt = (
            "Explain why the answer is wrong and teach the correct pattern.\n"
            f"Module: {module_id}\n"
            f"Question: {question}\n"
            f"Wrong answer: {wrong_answer}\n"
            f"Correct answer: {correct_answer}\n"
            f"Target language: {language}\n"
        )

        try:
            response = await self._client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                response_format={"type": "json_object"},
                temperature=0.4,
            )
            content = response.choices[0].message.content or ""
            payload = json.loads(content) if content else {}
            if not isinstance(payload, dict):
                payload = {}
            return self._normalize(payload, fallback)
        except Exception:
            return fallback

    async def chat(self, message: str, history: list[dict[str, Any]], module_id: str) -> dict[str, Any]:
        fallback = {
            "reply": "EN: I'm here to help—tell me a bit more. ZH: 我在这儿帮你，能再多说一点吗？"
        }
        if self._is_mock():
            return fallback

        system_prompt = (
            "You are a friendly language tutor. Keep responses short and helpful. "
            "Always respond in bilingual English + Chinese."
        )
        messages = [{"role": "system", "content": system_prompt}]
        for item in history or []:
            role = item.get("role")
            content = item.get("content") or item.get("text") or ""
            if role in {"user", "assistant"} and content:
                messages.append({"role": role, "content": content})
        messages.append(
            {
                "role": "user",
                "content": f"Module: {module_id}\nMessage: {message}",
            }
        )

        try:
            response = await self._client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.6,
            )
            reply = response.choices[0].message.content or ""
            return {"reply": reply.strip() or fallback["reply"]}
        except Exception:
            return fallback


_ai_tutor: AITutorService | None = None


def get_ai_tutor() -> AITutorService:
    global _ai_tutor
    if not _ai_tutor:
        _ai_tutor = AITutorService()
    return _ai_tutor
