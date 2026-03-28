class MockVoiceProvider:
    async def synthesize(self, text: str, voice: str = "nova", language: str = "en") -> bytes:
        # 返回最小有效mp3
        return b"\xff\xfb\x90\x00" + b"\x00" * 100

    async def transcribe(self, audio_bytes: bytes, language: str = "en") -> str:
        return "This is a mock transcription for testing purposes."

    async def assess_pronunciation(self, audio_bytes: bytes, reference_text: str, language: str = "en-US") -> dict:
        return {
            "score": 85.0,
            "accuracy": 88.0,
            "fluency": 83.0,
            "completeness": 90.0,
            "prosody": 79.0,
            "feedback": "Mock评测：发音良好，继续练习！",
            "words": [],
        }
