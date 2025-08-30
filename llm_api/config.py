# llm_api/config.py
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PORT = int(os.getenv("PORT", 8000))



class Settings(BaseSettings):
    OPENAI_API_KEY: str = OPENAI_API_KEY
    PORT: int = PORT
    MODEL_NAME: str = "gpt-4.1"
    TIMEOUT: int = 30
    VERSION: str = "0.1.0"

    class Config:
        env_file = ".env"

settings = Settings()
