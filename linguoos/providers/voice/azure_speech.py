import base64
import json
import httpx
import subprocess
import tempfile
import os
from linguoos.config import settings


class AzureSpeechProvider:
    def __init__(self):
        self.key = settings.azure_speech_key
        self.region = settings.azure_speech_region

    def _to_wav(self, audio_bytes: bytes) -> bytes:
        """把任意格式（webm/ogg/mp4）转成 Azure 需要的 PCM WAV 16kHz mono"""
        try:
            with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as fin:
                fin.write(audio_bytes)
                fin_path = fin.name
            fout_path = fin_path.replace(".webm", ".wav")
            subprocess.run(
                ["ffmpeg", "-y", "-i", fin_path,
                 "-ar", "16000", "-ac", "1", "-f", "wav", fout_path],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30
            )
            with open(fout_path, "rb") as f:
                wav = f.read()
            os.unlink(fin_path)
            os.unlink(fout_path)
            return wav
        except Exception:
            return audio_bytes  # fallback 原始数据

    async def assess_pronunciation(self, audio_bytes: bytes, reference_text: str, language: str = "en-US") -> dict:
        # 转 WAV
        wav_bytes = self._to_wav(audio_bytes)

        assessment_config = base64.b64encode(
            json.dumps({
                "ReferenceText": reference_text,
                "GradingSystem": "HundredMark",
                "Dimension": "Comprehensive",
                "EnableMiscue": True,
            }).encode()
        ).decode()

        url = f"https://{self.region}.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1"
        params = {"language": language, "format": "detailed"}
        headers = {
            "Ocp-Apim-Subscription-Key": self.key,
            "Content-Type": "audio/wav; codecs=audio/pcm; samplerate=16000",
            "Pronunciation-Assessment": assessment_config,
        }
        try:
            async with httpx.AsyncClient(verify=False, timeout=30) as client:
                resp = await client.post(url, params=params, headers=headers, content=wav_bytes)
            if resp.status_code != 200:
                return self._fallback()
            data = resp.json()
            nb = data.get("NBest", [{}])[0]
            pa = nb.get("PronunciationAssessment", {})
            words = [
                {
                    "word": w.get("Word", ""),
                    "score": round(w.get("PronunciationAssessment", {}).get("AccuracyScore", 0)),
                    "error_type": w.get("PronunciationAssessment", {}).get("ErrorType", "None"),
                }
                for w in nb.get("Words", [])
            ]
            total = round(pa.get("PronScore", 0))
            return {
                "scores": {
                    "total": total,
                    "accuracy": round(pa.get("AccuracyScore", 0)),
                    "fluency": round(pa.get("FluencyScore", 0)),
                    "completeness": round(pa.get("CompletenessScore", 0)),
                    "intonation": round(pa.get("ProsodyScore", 0)),
                },
                "words": words,
                "feedback": self._generate_feedback(total),
            }
        except Exception:
            return self._fallback()

    def _fallback(self):
        return {
            "scores": {"total": 0, "accuracy": 0, "fluency": 0, "completeness": 0, "intonation": 0},
            "words": [],
            "feedback": "评测服务暂时不可用，请检查网络或稍后重试",
        }

    def _generate_feedback(self, score: float) -> str:
        if score >= 90: return "发音非常标准！继续保持 🌟"
        if score >= 75: return "发音不错，注意个别音节的准确性 👍"
        if score >= 60: return "基本可以理解，建议多练习流利度 💪"
        return "需要加强练习，重点注意准确性和语调 📚"

    async def synthesize(self, text: str, voice: str = "en-US-JennyNeural", language: str = "en") -> bytes:
        url = f"https://{self.region}.tts.speech.microsoft.com/cognitiveservices/v1"
        ssml = f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="{language}"><voice name="{voice}">{text}</voice></speak>'
        headers = {
            "Ocp-Apim-Subscription-Key": self.key,
            "Content-Type": "application/ssml+xml",
            "X-Microsoft-OutputFormat": "audio-16khz-128kbitrate-mono-mp3",
        }
        async with httpx.AsyncClient(verify=False, timeout=30) as client:
            resp = await client.post(url, headers=headers, content=ssml.encode())
            return resp.content
