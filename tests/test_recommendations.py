import pytest
from app.services.recommendation_engine import RecommendationEngine

def test_recommendation_engine():
    engine = RecommendationEngine()
    response = engine.get_recommendations("Data Scientist", "US", "O*NET")
    assert response.job_title == "Data Scientist"
    assert response.framework == "O*NET"
    assert len(response.hard_skills) > 0
    assert len(response.soft_skills) > 0