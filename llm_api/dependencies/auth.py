from fastapi import HTTPException, Header
from datetime import datetime

# 模拟用户 token 数据库
user_tokens = {
    "user1_token": {"calls_today": 0, "last_reset": datetime.now()},
    "user2_token": {"calls_today": 0, "last_reset": datetime.now()}
}

def verify_token(x_api_token: str = Header(...)):
    if x_api_token not in user_tokens:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user_tokens[x_api_token]  # Return user info