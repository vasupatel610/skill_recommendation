import pytest
from app.services.rag_service import RAGService

def test_rag_query():
    rag = RAGService()
    results = rag.query("Skills for Data Scientist", "O*NET", n_results=2)
    assert isinstance(results, list)
    assert len(results) <= 2