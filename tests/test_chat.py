# tests/test_chat.py
import pytest
from fastapi.testclient import TestClient
from llm_api.main import app
from llm_api.services.chat_service import chat_endpoint

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
    response = client.post("/chat", json={"prompt": "Hi"})
    assert response.status_code == 200
    assert "response" in response.json()
