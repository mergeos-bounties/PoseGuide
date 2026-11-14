import pytest
from fastapi.testclient import TestClient
from src.poseguide.api.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_recommend_endpoint():
    payload = {"tags": ["beach", "standing"]}
    response = client.post("/guide/recommend", json=payload)
    assert response.status_code == 200
    assert "recommendations" in response.json()
    assert len(response.json()["recommendations"]) > 0

def test_score_endpoint():
    payload = {
        "subject_landmarks": {"nose": [0.5, 0.5], "left_shoulder": [0.4, 0.6]},
        "target_pose_id": "arms_crossed"
    }
    response = client.post("/guide/score", json=payload)
    assert response.status_code == 200
    assert "score" in response.json()
    assert "is_match" in response.json()

def test_invalid_recommend_payload():
    # Missing required 'tags' field
    response = client.post("/guide/recommend", json={})
    assert response.status_code == 422
