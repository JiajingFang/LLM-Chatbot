# llm_api/main.py
from fastapi import FastAPI, Depends
from llm_api.config import settings
from llm_api.services.chat_service import chat_endpoint

app = FastAPI(title="LLM API", version="0.1.0")

# 示例路由
@app.post("/chat")
async def chat(prompt: str):
    return await chat_endpoint(prompt)

@app.get("/health")
def health():
    return {"status": "ok", "version": settings.VERSION}