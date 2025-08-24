# llm_api/main.py
from fastapi import FastAPI, Depends
from llm_api.config import settings
from pydantic import BaseModel
from llm_api.services.chat_service import chat_endpoint

app = FastAPI(title="LLM API", version="0.1.0")

class ChatRequest(BaseModel):
    prompt: str

# 示例路由
@app.post("/chat")
async def chat(request: ChatRequest):
    return await chat_endpoint(request.prompt)

@app.get("/health")
def health():
    return {"status": "ok", "version": settings.VERSION}