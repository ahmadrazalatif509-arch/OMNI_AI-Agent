import io
from openai import OpenAI
from app.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def transcribe_audio_file(file_bytes: bytes, filename: str = "audio.wav") -> str:
    """Whisper API: صارف کی آواز کو پڑھ کر ٹیکسٹ میں تبدیل کرتا ہے"""
    audio_file = io.BytesIO(file_bytes)
    audio_file.name = filename
    
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )
    return transcript.text

def text_to_speech_file(text: str, voice: str = "alloy") -> bytes:
    """OpenAI TTS API: AI کے جواب کو قدرتی آواز (Audio Stream) میں بدلتا ہے"""
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text
    )
    return response.content