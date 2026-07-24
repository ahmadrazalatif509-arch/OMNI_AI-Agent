from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "OMNI AI"
    OPENAI_API_KEY: str = ""
    LUMA_API_KEY: str = ""
    DATABASE_URL: str = "sqlite:///./omni_ai.db"

    class Config:
        env_file = ".env"

settings = Settings()