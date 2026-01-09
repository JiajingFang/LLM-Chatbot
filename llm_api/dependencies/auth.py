from fastapi import HTTPException, Header, Depends
from datetime import datetime, timezone
from typing import Dict
from llm_api.utils.jwt import verify_token as verify_jwt_token
from llm_api.models.user_repository import UserRepository
from llm_api.config import settings

# Initialize user repository
_user_repo: UserRepository = None


def get_user_repository() -> UserRepository:
    """Get or create user repository instance"""
    global _user_repo
    if _user_repo is None:
        _user_repo = UserRepository(settings.MONGO_URI, settings.MONGO_DB)
    return _user_repo


async def verify_token(
    authorization: str = Header(..., description="Bearer token"),
    user_repo: UserRepository = Depends(get_user_repository)
) -> Dict:
    """Verify JWT token and return user info"""
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authentication scheme")
    
    token = authorization.split("Bearer ")[1].strip()
    payload = verify_jwt_token(token)
    
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    username = payload.get("sub")  # JWT standard uses 'sub' for subject
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    
    # Get user from database
    user = await user_repo.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    # Convert last_reset to datetime if it's a string
    last_reset = user.get("last_reset")
    if isinstance(last_reset, str):
        last_reset = datetime.fromisoformat(last_reset.replace('Z', '+00:00'))
    elif last_reset is None:
        last_reset = datetime.now(timezone.utc)
    
    # Return user info in the format expected by existing endpoints
    return {
        "user_name": user["username"],
        "calls_today": user.get("calls_today", 0),
        "last_reset": last_reset,
    }