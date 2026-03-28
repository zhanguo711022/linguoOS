import io
from openai import AsyncOpenAI
from linguoos.config import settings


class OpenAIVoiceProvider:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)

    async def synthesize(self, text: str, voice: str = "nova", language: str = "en") -> bytes:
        response = await self.client.audio.speech.create(
            model="tts-1", voice=voice, input=text
        )
        return response.content

    async def transcribe(self, audio_bytes: bytes, language: str = "en") -> str:
        audio_file = io.BytesIO(audio_bytes)
        audio_file.name = "audio.webm"
        transcript = await self.client.audio.transcriptions.create(
            model="whisper-1", file=audio_file, language=language[:2]
        )
        return transcript.text
