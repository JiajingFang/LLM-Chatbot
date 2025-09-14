# llm_api/config.py
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PORT = int(os.getenv("PORT", 8000))
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")



class Settings(BaseSettings):
    OPENAI_API_KEY: str = OPENAI_API_KEY
    CLAUDE_API_KEY: str = CLAUDE_API_KEY
    PORT: int = PORT
    OPENAI_MODEL: str = "gpt-4.1"
    CLAUDE_API_MODEL: str = "claude-sonnet-4-20250514"
    TIMEOUT: int = 30
    VERSION: str = "0.1.0"

    class Config:
        env_file = ".env"

settings = Settings()
