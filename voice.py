from fastapi import APIRouter, UploadFile, File, Response
from pydantic import BaseModel
from app.services.voice_service import transcribe_audio_file, text_to_speech_file

router = APIRouter(prefix="/api/voice", tags=["Voice Generation"])

class TTSRequest(BaseModel):
    text: str
    voice: str = "alloy"  # Voices: alloy, echo, fable, onyx, nova, shimmer

@router.post("/stt")
async def speech_to_text(file: UploadFile = File(...)):
    """User کی ریکارڈ شدہ وائس فائل لے کر اس کا Text واپس کرتا ہے"""
    audio_bytes = await file.read()
    text = transcribe_audio_file(audio_bytes, filename=file.filename)
    return {"text": text}

@router.post("/tts")
async def text_to_speech(req: TTSRequest):
    """Text کو بائٹس (MP3) میں بدل کر بولتی ہوئی آواز بھیجتا ہے"""
    audio_data = text_to_speech_file(req.text, req.voice)
    return Response(content=audio_data, media_type="audio/mpeg")