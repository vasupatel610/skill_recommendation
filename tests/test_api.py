import pytest
import httpx
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_recommend_skills():
    response = client.post(
        "/recommend-skills",
        json={"job_title": "Data Scientist", "country": "US", "framework": "O*NET"}
    )
    assert response.status_code == 200
    assert "hard_skills" in response.json()
    assert "soft_skills" in response.json()

def test_job_description():
    response = client.get("/job-description/Data%20Scientist")
    assert response.status_code == 200
    assert "description" in response.json()