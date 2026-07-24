from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from APP.services.ai_service import stream_chat_response, extract_pdf_text

router = APIRouter(prefix="/api/chat", tags=["Chat"])

@router.post("/stream")
async def chat_stream(payload: dict):
    messages = payload.get("messages", [])
    return StreamingResponse(stream_chat_response(messages), media_type="text/event-stream")

@router.post("/analyze-file")
async def analyze_file(
    file: UploadFile = File(...),
    prompt: str = Form("Analyze this file in detail.")
):
    contents = await file.read()
    text = ""
    if file.filename.endswith(".pdf"):
        import io
        text = extract_pdf_text(io.BytesIO(contents))
    else:
        text = contents.decode("utf-8", errors="ignore")

    messages = [
        {"role": "system", "content": f"File Content Context:\n{text[:8000]}"},
        {"role": "user", "content": prompt}
    ]
    return StreamingResponse(stream_chat_response(messages), media_type="text/event-stream")