import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestAPI:
    """Test API endpoints"""
    
    def test_root_endpoint(self):
        """Test root endpoint returns welcome message"""
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()
        assert "ResearchMate AI" in response.json()["message"]
    
    def test_query_endpoint_structure(self):
        """Test query endpoint accepts correct structure"""
        response = client.post(
            "/api/v1/query",
            json={"query": "What is machine learning?"}
        )
        # Should return 200 or 500 (if API key issues), but not 422 (validation error)
        assert response.status_code in [200, 500]
    
    def test_query_endpoint_validation(self):
        """Test query endpoint validates input"""
        # Missing query field
        response = client.post("/api/v1/query", json={})
        assert response.status_code == 422  # Validation error
    
    def test_upload_endpoint_no_file(self):
        """Test upload endpoint without file"""
        response = client.post("/api/v1/upload")
        assert response.status_code == 422  # Missing required field
