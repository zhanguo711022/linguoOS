import base64
import json
import httpx
from linguoos.config import settings


class AzureSpeechProvider:
    def __init__(self):
        self.key = settings.azure_speech_key
        self.region = settings.azure_speech_region

    async def assess_pronunciation(self, audio_bytes: bytes, reference_text: str, language: str = "en-US") -> dict:
        assessment_config = base64.b64encode(
            json.dumps(
                {
                    "ReferenceText": reference_text,
                    "GradingSystem": "HundredMark",
                    "Dimension": "Comprehensive",
                    "EnableMiscue": True,
                }
            ).encode()
        ).decode()

        url = f"https://{self.region}.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1"
        params = {"language": language, "format": "detailed"}
        headers = {
            "Ocp-Apim-Subscription-Key": self.key,
            "Content-Type": "audio/wav; codecs=audio/pcm; samplerate=16000",
            "Pronunciation-Assessment": assessment_config,
        }
        async with httpx.AsyncClient(verify=False, timeout=30) as client:
            resp = await client.post(url, params=params, headers=headers, content=audio_bytes)
            if resp.status_code != 200:
                return {
                    "score": 0,
                    "accuracy": 0,
                    "fluency": 0,
                    "completeness": 0,
                    "prosody": 0,
                    "feedback": "评测服务暂时不可用",
                    "words": [],
                }
            data = resp.json()
            nb = data.get("NBest", [{}])[0]
            pa = nb.get("PronunciationAssessment", {})
            return {
                "score": pa.get("PronScore", 0),
                "accuracy": pa.get("AccuracyScore", 0),
                "fluency": pa.get("FluencyScore", 0),
                "completeness": pa.get("CompletenessScore", 0),
                "prosody": pa.get("ProsodyScore", 0),
                "feedback": self._generate_feedback(pa),
                "words": [
                    {
                        "word": w.get("Word", ""),
                        "accuracy": w.get("PronunciationAssessment", {}).get("AccuracyScore", 0),
                    }
                    for w in nb.get("Words", [])
                ],
            }

    def _generate_feedback(self, pa: dict) -> str:
        score = pa.get("PronScore", 0)
        if score >= 90:
            return "发音非常标准！继续保持 🌟"
        if score >= 75:
            return "发音不错，注意个别音节的准确性 👍"
        if score >= 60:
            return "基本可以理解，建议多练习流利度 💪"
        return "需要加强练习，重点注意准确性和语调 📚"

    async def synthesize(self, text: str, voice: str = "en-US-JennyNeural", language: str = "en") -> bytes:
        url = f"https://{self.region}.tts.speech.microsoft.com/cognitiveservices/v1"
        ssml = (
            f"""<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="{language}">"
            f"<voice name="{voice}">{text}</voice></speak>"""
        )
        headers = {
            "Ocp-Apim-Subscription-Key": self.key,
            "Content-Type": "application/ssml+xml",
            "X-Microsoft-OutputFormat": "audio-16khz-128kbitrate-mono-mp3",
        }
        async with httpx.AsyncClient(verify=False, timeout=30) as client:
            resp = await client.post(url, headers=headers, content=ssml.encode())
            return resp.content
