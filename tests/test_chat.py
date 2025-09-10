# tests/test_chat.py
import pytest
from fastapi.testclient import TestClient
from llm_api.main import app
from llm_api.services.chat_service import chat_endpoint
from datetime import datetime
from llm_api.dependencies.auth import verify_token 

def always_authenticated(x_api_token: str = None):
    return {"calls_today": 0, "last_reset": datetime.now()}

app.dependency_overrides[verify_token] = always_authenticated

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

@pytest.mark.asyncio
async def test_chat_endpoint(monkeypatch):
    async def fake_chat(prompt):
        return {"response": {"choices": [{"text": "Hello"}]}}
    monkeypatch.setattr("llm_api.services.chat_service.chat_endpoint", fake_chat)
    headers = {"x-api-token": "test_token"}
    response = client.post("/chat", json={"prompt": "Hi"}, headers=headers)
    assert response.status_code == 200
    assert "response" in response.json()
