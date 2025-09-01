# llm_api/main.py
from fastapi import FastAPI, Depends, Request, HTTPException, Header
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from llm_api.config import settings
from pydantic import BaseModel
from llm_api.services.chat_service import chat_endpoint
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from llm_api.dependencies.auth import verify_token


limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="LLM API", version="0.1.0")
app.state.limiter = limiter

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 可改为前端地址
    allow_methods=["*"],
    allow_headers=["*"],
)

# 捕获限流异常
@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request: Request, exc):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests, slow down!"}
    )


MAX_CALLS_PER_DAY = 100  # 每个 token 每天最多调用次数

class ChatRequest(BaseModel):
    prompt: str


# 示例路由
@app.post("/chat")
@limiter.limit("10/minute")
async def chat(request: Request, body: ChatRequest, user=Depends(verify_token)):
    now = datetime.now()
    if now.date() != user["last_reset"].date():
        user["calls_today"] = 0
        user["last_reset"] = now

    if user["calls_today"] >= MAX_CALLS_PER_DAY:
        raise HTTPException(status_code=429, detail="Daily call limit exceeded")
    if not body.prompt:
        raise HTTPException(status_code=400, detail="Question is required")
    
    try:
        response = await chat_endpoint(body.prompt)
        user["calls_today"] += 1
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/health")
def health():
    return {"status": "ok", "version": settings.VERSION}