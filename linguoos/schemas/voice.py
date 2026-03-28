from pydantic import BaseModel
from typing import List


class TTSRequest(BaseModel):
    text: str
    language: str = "en"
    voice: str = "nova"


class STTResponse(BaseModel):
    text: str
    language: str


class WordScore(BaseModel):
    word: str
    accuracy: float


class AssessResponse(BaseModel):
    score: float
    accuracy: float
    fluency: float
    completeness: float
    prosody: float
    feedback: str
    words: List[WordScore] = []
