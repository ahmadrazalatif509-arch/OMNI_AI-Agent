import json
from openai import OpenAI
from app.config import settings
from app.services.web_search import search_web
import pypdf

client = OpenAI(api_key=settings.OPENAI_API_KEY)

TOOLS_SPEC = [
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the live internet for recent facts, news, and real-time information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search engine query string"}
                },
                "required": ["query"]
            }
        }
    }
]

async def stream_chat_response(messages: list):
    """GPT-4o Streaming Chat & Code/Website Generation Logic"""
    system_instruction = {
        "role": "system",
        "content": (
            "You are OMNI AI, an advanced full-stack AI assistant. "
            "If the user asks to build a website, app, or write code (e.g. Python, React, HTML), "
            "generate complete, production-ready, clean code blocks. "
            "For full web pages, output raw executable HTML/CSS/JS inside ```html ... ``` blocks."
        )
    }
    
    full_messages = [system_instruction] + messages

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=full_messages,
        tools=TOOLS_SPEC,
        tool_choice="auto",
        stream=True
    )

    for chunk in response:
        delta = chunk.choices[0].delta
        if delta.content:
            yield f"data: {json.dumps({'content': delta.content})}\n\n"

    yield "data: [DONE]\n\n"

def extract_pdf_text(file_bytes) -> str:
    """PDF فائل سے ٹیکسٹ نکالنے کا فنکشن"""
    reader = pypdf.PdfReader(file_bytes)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text