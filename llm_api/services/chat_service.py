# llm_api/services/chat_service.py
from llm_api.config import settings
from llm_api.utils.logger import get_logger
import httpx
import anthropic
import asyncio

logger = get_logger(__name__)

client = anthropic.Anthropic(
    api_key=settings.CLAUDE_API_KEY
)

async def call_claude(message):
    response = client.messages.create(
        model=settings.CLAUDE_API_MODEL, 
        max_tokens=1024,
        messages=[
            {"role": "user", "content": message}
        ]
    )
    logger.info("Claude response received")
    return response.content[0].text

async def call_openai(prompt):
    payload = {
        "model": settings.OPENAI_MODEL,
        "input": prompt
    }
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {settings.OPENAI_API_KEY}",}
    async with httpx.AsyncClient(timeout=settings.TIMEOUT) as client:
        response = await client.post("https://api.openai.com/v1/responses", json=payload, headers=headers)
        if response.status_code != 200:
            logger.error(f"OpenAI API error: {response.status_code} - {response.text}")
            return {"error": "OpenAI API request failed"}
        else:
            data = response.json()["output"][0]["content"][0]["text"]
            logger.info("OpenAI response received")
            return data

async def chat_endpoint(prompt: str) -> dict:
    openai_task = call_openai(prompt)
    claude_task = call_claude(prompt)
    response_openai, response_claude = await asyncio.gather(openai_task, claude_task)
    logger.info("Both OpenAI and Claude responses received")
    return {"response": {"openai": response_openai, "anthropic": response_claude}}

