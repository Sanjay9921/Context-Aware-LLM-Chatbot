from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_root():
    res = client.get("/")
    assert res.status_code == 200
    assert res.json() == {"message": "LLM Chatbot API is running"}

def test_post_query_response():
    payload = {
        "prompt": "What is the capital of Germany?",
        "model": "meta-llama/Meta-Llama-3-70B-Instruct-Turbo"
    }
    res = client.post("/query", json=payload)

    assert res.status_code == 200
    data = res.json()
    assert "Simulated answer" in data["response"]
    assert data["model"] == payload["model"]
    assert data["latency"] < 5
