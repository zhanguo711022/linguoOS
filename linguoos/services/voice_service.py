from linguoos.config import settings
from linguoos.providers.voice.openai_voice import OpenAIVoiceProvider
from linguoos.providers.voice.azure_speech import AzureSpeechProvider
from linguoos.providers.voice.mock_voice import MockVoiceProvider


class VoiceService:
    def __init__(self):
        self.mock = MockVoiceProvider()
        self._openai = None
        self._azure = None

    @property
    def openai(self):
        if not self._openai:
            self._openai = OpenAIVoiceProvider()
        return self._openai

    @property
    def azure(self):
        if not self._azure:
            self._azure = AzureSpeechProvider()
        return self._azure

    def _is_mock(self):
        return settings.provider == "mock" or not settings.openai_api_key

    async def text_to_speech(self, text: str, language: str = "en", voice: str = "nova") -> bytes:
        if self._is_mock():
            return await self.mock.synthesize(text, voice, language)
        try:
            return await self.openai.synthesize(text, voice, language)
        except Exception:
            return await self.mock.synthesize(text, voice, language)

    async def speech_to_text(self, audio_bytes: bytes, language: str = "en") -> str:
        if self._is_mock():
            return await self.mock.transcribe(audio_bytes, language)
        try:
            return await self.openai.transcribe(audio_bytes, language)
        except Exception:
            return await self.mock.transcribe(audio_bytes, language)

    async def assess_pronunciation(self, audio_bytes: bytes, reference_text: str, language: str = "en") -> dict:
        if self._is_mock() or not settings.azure_speech_key:
            return await self.mock.assess_pronunciation(audio_bytes, reference_text, language)
        try:
            lang_code = "en-US" if language.startswith("en") else "zh-CN" if language.startswith("zh") else language
            return await self.azure.assess_pronunciation(audio_bytes, reference_text, lang_code)
        except Exception:
            return await self.mock.assess_pronunciation(audio_bytes, reference_text, language)


_voice_service = None


def get_voice_service() -> VoiceService:
    global _voice_service
    if not _voice_service:
        _voice_service = VoiceService()
    return _voice_service
