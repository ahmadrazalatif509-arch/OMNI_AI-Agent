from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.services.ai_service import stream_chat_response

router = APIRouter(prefix="/api/builder", tags=["Website & Code Generation"])

class CodePrompt(BaseModel):
    prompt: str
    language: str = "html"

@router.post("/generate")
async def generate_code(req: CodePrompt):
    """پورے ویب پیج یا React/Python کوڈ کی جنریشن کے لیے"""
    messages = [{
        "role": "user",
        "content": (
            f"Write a complete, single-file runnable {req.language} application for: '{req.prompt}'. "
            "Output pure code inside markdown backticks."
        )
    }]
    return StreamingResponse(stream_chat_response(messages), media_type="text/event-stream")