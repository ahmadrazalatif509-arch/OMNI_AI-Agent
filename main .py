from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from APP.database import init_db
from APP.routers import chat, voice, media

app = FastAPI(title="OMNI AI Engine", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()

app.include_router(chat.router)
app.include_router(voice.router)
app.include_router(media.router)

@app.get("/")
def root():
    return {"status": "online", "system": "OMNI AI Central Core"}