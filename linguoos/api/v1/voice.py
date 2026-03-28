from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import StreamingResponse
import io
from linguoos.services.voice_service import get_voice_service
from linguoos.schemas.voice import TTSRequest, STTResponse, AssessResponse

router = APIRouter(prefix="/api/v1/voice", tags=["voice"])


@router.post("/tts")
async def text_to_speech(req: TTSRequest):
    svc = get_voice_service()
    audio = await svc.text_to_speech(req.text, req.language, req.voice)
    return StreamingResponse(
        io.BytesIO(audio),
        media_type="audio/mpeg",
        headers={"Content-Disposition": "inline; filename=speech.mp3"},
    )


@router.post("/stt", response_model=STTResponse)
async def speech_to_text(audio: UploadFile = File(...), language: str = Form("en")):
    svc = get_voice_service()
    audio_bytes = await audio.read()
    text = await svc.speech_to_text(audio_bytes, language)
    return STTResponse(text=text, language=language)


@router.post("/assess", response_model=AssessResponse)
async def assess_pronunciation(
    audio: UploadFile = File(...),
    reference_text: str = Form(...),
    language: str = Form("en"),
):
    svc = get_voice_service()
    audio_bytes = await audio.read()
    result = await svc.assess_pronunciation(audio_bytes, reference_text, language)
    return AssessResponse(**result)


@router.get("/voices")
async def list_voices():
    return {
        "voices": [
            {
                "id": "nova",
                "name": "Nova",
                "language": "en",
                "gender": "female",
                "preview": "Hi! I am Nova, your LinguoOS tutor.",
            },
            {
                "id": "alloy",
                "name": "Alloy",
                "language": "en",
                "gender": "neutral",
                "preview": "Hello! Let us practice together.",
            },
            {
                "id": "echo",
                "name": "Echo",
                "language": "en",
                "gender": "male",
                "preview": "Good day! Ready to learn?",
            },
            {
                "id": "en-US-JennyNeural",
                "name": "Jenny (Azure)",
                "language": "en",
                "gender": "female",
                "preview": "",
            },
            {
                "id": "zh-CN-XiaoxiaoNeural",
                "name": "晓晓 (Azure)",
                "language": "zh",
                "gender": "female",
                "preview": "你好！我是你的中文老师晓晓。",
            },
        ]
    }
