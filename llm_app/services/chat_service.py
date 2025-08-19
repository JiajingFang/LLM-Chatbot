# llm_api/services/chat_service.py
from llm_api.config import settings
from llm_api.utils.logger import get_logger
import httpx

logger = get_logger(__name__)

async def chat_endpoint(prompt: str) -> dict:
    payload = {
        "model": settings.MODEL_NAME,
        "prompt": prompt,
        "max_tokens": 150,
    }
    headers = {"Authorization": f"Bearer {settings.OPENAI_API_KEY}"}
    async with httpx.AsyncClient(timeout=settings.TIMEOUT) as client:
        response = await client.post("https://api.openai.com/v1/completions", json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        logger.info("LLM response received")
        return {"response": data}

# 可根据实际逻辑调整
