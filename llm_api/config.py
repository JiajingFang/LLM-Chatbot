# llm_api/config.py
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str = "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"
    MODEL_NAME: str = "gpt-4.1"
    TIMEOUT: int = 30
    VERSION: str = "0.1.0"

    class Config:
        env_file = ".env"

settings = Settings()
