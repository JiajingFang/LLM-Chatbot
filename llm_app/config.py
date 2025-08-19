# llm_api/config.py
import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    MODEL_NAME: str = "gpt-4"
    TIMEOUT: int = 30
    VERSION: str = "0.1.0"

    class Config:
        env_file = ".env"

settings = Settings()
