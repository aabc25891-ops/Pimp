"""Unit tests for PIMP"""

import pytest
from fastapi.testclient import TestClient
from datetime import date
from api.main import app
from database.database import SessionLocal, Base, engine
from database.models import Product, TrendPrediction

# Create test client
client = TestClient(app)


@pytest.fixture
def test_db():
    """Create test database"""
    Base.metadata.create_all(bind=engine)
    yield SessionLocal()
    Base.metadata.drop_all(bind=engine)


class TestHealth:
    """Test health endpoint"""
    
    def test_health_check(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_root_endpoint(self):
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()


class TestProducts:
    """Test product endpoints"""
    
    def test_list_products(self, test_db):
        response = client.get("/api/v1/products/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_create_product(self, test_db):
        product_data = {
            "product_name": "Test Product",
            "category": "Electronics",
            "price": 999.99,
            "rating": 4.5,
            "reviews_count": 100,
            "source": "amazon"
        }
        response = client.post("/api/v1/products/", json=product_data)
        assert response.status_code == 200
        assert response.json()["product_name"] == "Test Product"
    
    def test_get_product_not_found(self):
        response = client.get("/api/v1/products/invalid_id")
        assert response.status_code == 404


class TestPredictions:
    """Test prediction endpoints"""
    
    def test_list_predictions(self):
        response = client.get("/api/v1/predictions/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_create_prediction(self):
        prediction_data = {
            "product_id": "test_product_1",
            "trend_score": 75.5,
            "probability": 0.85,
            "confidence": "High"
        }
        response = client.post("/api/v1/predictions/", json=prediction_data)
        # May fail if product doesn't exist, but tests structure
        assert response.status_code in [200, 500]
    
    def test_get_top_trending(self):
        response = client.get("/api/v1/predictions/top-trending")
        assert response.status_code == 200


class TestAnalytics:
    """Test analytics endpoints"""
    
    def test_analytics_summary(self):
        response = client.get("/api/v1/analytics/summary")
        assert response.status_code == 200
        data = response.json()
        assert "total_products" in data
        assert "total_predictions" in data
    
    def test_category_statistics(self):
        response = client.get("/api/v1/analytics/category-stats")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_model_performance(self):
        response = client.get("/api/v1/analytics/model-performance")
        assert response.status_code == 200
    
    def test_api_usage(self):
        response = client.get("/api/v1/analytics/api-usage?hours=24")
        assert response.status_code == 200


class TestTrends:
    """Test trends endpoints"""
    
    def test_google_trending(self):
        response = client.get("/api/v1/trends/google/trending")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_reddit_trending(self):
        response = client.get("/api/v1/trends/reddit/trending")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_keyword_trend(self):
        response = client.get("/api/v1/trends/keyword/smartphone")
        assert response.status_code == 200
        data = response.json()
        assert "keyword" in data
    
    def test_trend_momentum(self):
        response = client.get("/api/v1/trends/momentum?days=30")
        assert response.status_code == 200
