from fastapi import APIRouter
from pydantic import BaseModel
from app.services.media_service import generate_dalle_image, generate_ai_video

router = APIRouter(prefix="/api/media", tags=["Media Generation"])

class GenRequest(BaseModel):
    prompt: str

@router.post("/generate-image")
async def make_image(req: GenRequest):
    """Text to Image API Endpoint"""
    url = generate_dalle_image(req.prompt)
    return {"url": url}

@router.post("/generate-video")
async def make_video(req: GenRequest):
    """Text to Video API Endpoint"""
    url = generate_ai_video(req.prompt)
    return {"url": url}