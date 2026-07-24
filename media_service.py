import requests
from openai import OpenAI
from app.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_dalle_image(prompt: str) -> str:
    """DALL-E 3: اعلیٰ کوالٹی تصاویر تیار کرنے کے لیے"""
    res = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1
    )
    return res.data[0].url

def generate_ai_video(prompt: str) -> str:
    """
    Text-to-Video Engine: Luma/Runway API کو کال کرتا ہے۔ 
    اگر API Key نہ ہو تو ڈیمو/ٹیسٹنگ کے لیے سیمپل MP4 کا پاتھ دیتا ہے۔
    """
    if settings.LUMA_API_KEY:
        try:
            headers = {"Authorization": f"Bearer {settings.LUMA_API_KEY}"}
            resp = requests.post(
                "https://api.lumalabs.ai/dream-machine/v1/generations",
                json={"prompt": prompt},
                headers=headers
            )
            data = resp.json()
            return data.get("assets", {}).get("video", "")
        except Exception as e:
            print(f"Video Gen Error: {e}")

    # fallback testing stream video
    return "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4"