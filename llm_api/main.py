# llm_api/main.py
from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from llm_api.config import settings
from pydantic import BaseModel
from llm_api.services.chat_service import chat_endpoint
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone, timedelta
from llm_api.dependencies.auth import verify_token, get_user_repository
from llm_api.services.comparison import compare_with_openai
from llm_api.models.user_repository import UserRepository
from llm_api.utils.jwt import create_access_token
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

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str

class ComparisonResponse(BaseModel):
    claude_response: str
    openai_response: str
    summary: str
    comparison: str
    processing_time: float
    method_used: str


@app.post("/chat")
@limiter.limit("10/minute")
async def chat(
    request: Request,
    body: ChatRequest,
    user=Depends(verify_token),
    user_repo: UserRepository = Depends(get_user_repository)
):
    now = datetime.now(timezone.utc)
    if isinstance(user["last_reset"], datetime):
        last_reset = user["last_reset"]
    else:
        last_reset = datetime.now(timezone.utc)
    
    if now.date() != last_reset.date():
        user["calls_today"] = 0
        user["last_reset"] = now
        # Update in database
        await user_repo.update_user_usage(user["user_name"], 0, now)

    if user["calls_today"] >= MAX_CALLS_PER_DAY:
        raise HTTPException(status_code=429, detail="Daily call limit exceeded")
    if not body.prompt:
        raise HTTPException(status_code=400, detail="Question is required")
    
    try:
        response = await chat_endpoint(body.prompt, user["user_name"])
        user["calls_today"] += 1
        # Update in database
        await user_repo.update_user_usage(user["user_name"], user["calls_today"], user["last_reset"])
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/health")
def health():
    return {"status": "ok", "version": settings.VERSION}


@app.post("/register", response_model=TokenResponse)
async def register(
    body: RegisterRequest,
    user_repo: UserRepository = Depends(get_user_repository)
):
    """Register a new user"""
    if not body.username or not body.password:
        raise HTTPException(status_code=400, detail="Username and password are required")
    
    if len(body.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
    
    try:
        user = await user_repo.create_user(body.username, body.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")
    
    # Create access token
    access_token = create_access_token(data={"sub": user["username"]})
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        username=user["username"]
    )


@app.post("/login", response_model=TokenResponse)
async def login(
    body: LoginRequest,
    user_repo: UserRepository = Depends(get_user_repository)
):
    """Login and get access token"""
    if not body.username or not body.password:
        raise HTTPException(status_code=400, detail="Username and password are required")
    
    user = await user_repo.authenticate_user(body.username, body.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    # Create access token
    access_token = create_access_token(data={"sub": user["username"]})
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        username=user["username"]
    )


@app.post("/compare", response_model=ComparisonResponse)
@limiter.limit("10/minute")
async def compare_llms(
    request: Request,
    body: ChatRequest,
    user=Depends(verify_token),
    user_repo: UserRepository = Depends(get_user_repository)
):
    now = datetime.now(timezone.utc)
    if isinstance(user["last_reset"], datetime):
        last_reset = user["last_reset"]
    else:
        last_reset = datetime.now(timezone.utc)
    
    if now.date() != last_reset.date():
        user["calls_today"] = 0
        user["last_reset"] = now
        # Update in database
        await user_repo.update_user_usage(user["user_name"], 0, now)

    if user["calls_today"] >= MAX_CALLS_PER_DAY:
        raise HTTPException(status_code=429, detail="Daily call limit exceeded")
    if not body.prompt:
        raise HTTPException(status_code=400, detail="Question is required")
 
    
    try:
        response = await chat_endpoint(body.prompt, user["user_name"])
        user["calls_today"] += 1
        # Update in database
        await user_repo.update_user_usage(user["user_name"], user["calls_today"], user["last_reset"])
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
