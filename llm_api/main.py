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
from llm_api.services.comparison import compare_with_openai
import time


limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="LLM API", version="0.1.0")
app.state.limiter = limiter

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
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


MAX_CALLS_PER_DAY = 100  # max calls per user per day

class ChatRequest(BaseModel):
    prompt: str

class ComparisonResponse(BaseModel):
    claude_response: str
    openai_response: str
    summary: str
    comparison: str
    processing_time: float
    method_used: str


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
        response = await chat_endpoint(body.prompt, user["user_name"])
        user["calls_today"] += 1
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/health")
def health():
    return {"status": "ok", "version": settings.VERSION}


@app.post("/compare", response_model=ComparisonResponse)
@limiter.limit("10/minute")
async def compare_llms(request: Request, body: ChatRequest, user=Depends(verify_token)):
    now = datetime.now()
    if now.date() != user["last_reset"].date():
        user["calls_today"] = 0
        user["last_reset"] = now

    if user["calls_today"] >= MAX_CALLS_PER_DAY:
        raise HTTPException(status_code=429, detail="Daily call limit exceeded")
    if not body.prompt:
        raise HTTPException(status_code=400, detail="Question is required")
 
    
    try:
        response = await chat_endpoint(body.prompt, user["user_name"])
        user["calls_today"] += 1
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    if response is None or "response" not in response:
        raise HTTPException(status_code=500, detail="No response from LLMs")
    anth_resp, openai_resp = response.get("response").get("anthropic"), response.get("response").get("openai")
    if not anth_resp or not openai_resp:
        raise HTTPException(status_code=500, detail="One of the LLM responses is empty") 
    try:  
        # Compare and summarize
        start_time = time.time()
        comparison_result = await compare_with_openai(anth_resp, openai_resp)
        method_used = "api"
        
        processing_time = time.time() - start_time
        
        return ComparisonResponse(
            claude_response=anth_resp,
            openai_response=openai_resp,
            summary=comparison_result["summary"],
            comparison=comparison_result["comparison"],
            processing_time=processing_time,
            method_used=method_used
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Request failed: {e}")
