# llm_api/services/chat_service.py
from llm_api.config import settings
from llm_api.utils.logger import get_logger
import httpx

logger = get_logger(__name__)

async def chat_endpoint(prompt: str) -> dict:
    payload = {
        "model": settings.MODEL_NAME,
        "input": prompt
    }
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {settings.OPENAI_API_KEY}",}
    async with httpx.AsyncClient(timeout=settings.TIMEOUT) as client:
        response = await client.post("https://api.openai.com/v1/responses", json=payload, headers=headers)
        if response.status_code != 200:
            logger.error(f"LLM API error: {response.status_code} - {response.text}")
            return {"error": "LLM API request failed"}
        else:
            data = response.json()["output"][0]["content"][0]["text"]
        # data = response.json()
        logger.info("LLM response received")
        return {"response": data}

# 可根据实际逻辑调整
