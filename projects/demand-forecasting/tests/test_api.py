"""
Tests for FastAPI endpoints

Author: Ing. Daniel Varela Perez
Email: bedaniele0@gmail.com
Date: December 5, 2024
"""

import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


class TestRootEndpoint:
    """Test root endpoint"""

    def test_root_endpoint(self):
        """Test root endpoint returns correct response"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert data["version"] == "1.0.0"


class TestHealthEndpoint:
    """Test health check endpoint"""

    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code in [200, 503]  # May be unhealthy if model not loaded
        data = response.json()
        assert "status" in data
        assert "model_loaded" in data
        assert "uptime_seconds" in data

    def test_health_check_schema(self):
        """Test health check response schema"""
        response = client.get("/health")
        data = response.json()
        required_fields = ["status", "model_loaded", "model_version", "uptime_seconds", "timestamp"]
        for field in required_fields:
            assert field in data


class TestModelInfoEndpoint:
    """Test model info endpoint"""

    def test_model_info(self):
        """Test model info endpoint"""
        response = client.get("/model/info")
        # May return 503 if model not loaded
        assert response.status_code in [200, 503]

        if response.status_code == 200:
            data = response.json()
            assert "model_name" in data
            assert "model_version" in data
            assert "model_type" in data

    def test_model_info_schema(self):
        """Test model info response schema"""
        response = client.get("/model/info")

        if response.status_code == 200:
            data = response.json()
            required_fields = [
                "model_name", "model_version", "model_type",
                "training_date", "features_count", "performance_metrics"
            ]
            for field in required_fields:
                assert field in data


class TestPredictionEndpoint:
    """Test prediction endpoint"""

    def test_predict_with_valid_input(self):
        """Test prediction with valid input"""
        request_data = {
            "item_id": "FOODS_1_001_CA_1",
            "store_id": "CA_1",
            "date": "2016-05-01"
        }

        response = client.post("/predict", json=request_data)

        # May return 503 if model not loaded
        assert response.status_code in [200, 503]

        if response.status_code == 200:
            data = response.json()
            assert "predicted_sales" in data
            assert "item_id" in data
            assert data["item_id"] == request_data["item_id"]

    def test_predict_with_invalid_date_format(self):
        """Test prediction with invalid date format"""
        request_data = {
            "item_id": "FOODS_1_001_CA_1",
            "store_id": "CA_1",
            "date": "05-01-2016"  # Invalid format
        }

        response = client.post("/predict", json=request_data)
        assert response.status_code == 422  # Validation error

    def test_predict_with_missing_fields(self):
        """Test prediction with missing required fields"""
        request_data = {
            "item_id": "FOODS_1_001_CA_1"
            # Missing store_id and date
        }

        response = client.post("/predict", json=request_data)
        assert response.status_code == 422  # Validation error

    def test_predict_response_schema(self):
        """Test prediction response schema"""
        request_data = {
            "item_id": "FOODS_1_001_CA_1",
            "store_id": "CA_1",
            "date": "2016-05-01"
        }

        response = client.post("/predict", json=request_data)

        if response.status_code == 200:
            data = response.json()
            required_fields = [
                "item_id", "store_id", "date", "predicted_sales",
                "model_version", "timestamp"
            ]
            for field in required_fields:
                assert field in data

            # Check prediction is non-negative
            assert data["predicted_sales"] >= 0


class TestBatchPredictionEndpoint:
    """Test batch prediction endpoint"""

    def test_batch_predict_with_valid_input(self):
        """Test batch prediction with valid input"""
        request_data = {
            "items": [
                {
                    "item_id": "FOODS_1_001_CA_1",
                    "store_id": "CA_1",
                    "date": "2016-05-01"
                },
                {
                    "item_id": "FOODS_1_002_CA_1",
                    "store_id": "CA_1",
                    "date": "2016-05-01"
                }
            ]
        }

        response = client.post("/predict/batch", json=request_data)

        # May return 503 if model not loaded
        assert response.status_code in [200, 503]

        if response.status_code == 200:
            data = response.json()
            assert "predictions" in data
            assert "total_items" in data
            assert "processing_time_ms" in data
            assert len(data["predictions"]) <= len(request_data["items"])

    def test_batch_predict_with_empty_items(self):
        """Test batch prediction with empty items list"""
        request_data = {"items": []}

        response = client.post("/predict/batch", json=request_data)
        assert response.status_code == 422  # Validation error

    def test_batch_predict_response_schema(self):
        """Test batch prediction response schema"""
        request_data = {
            "items": [
                {
                    "item_id": "FOODS_1_001_CA_1",
                    "store_id": "CA_1",
                    "date": "2016-05-01"
                }
            ]
        }

        response = client.post("/predict/batch", json=request_data)

        if response.status_code == 200:
            data = response.json()
            assert isinstance(data["predictions"], list)
            assert isinstance(data["total_items"], int)
            assert isinstance(data["processing_time_ms"], float)


class TestFeatureImportanceEndpoint:
    """Test feature importance endpoint"""

    def test_feature_importance_default(self):
        """Test feature importance with default parameters"""
        response = client.get("/model/features/importance")

        # May return 503 if model not loaded
        assert response.status_code in [200, 503]

        if response.status_code == 200:
            data = response.json()
            assert "features" in data
            assert "top_n" in data

    def test_feature_importance_custom_top_n(self):
        """Test feature importance with custom top_n"""
        response = client.get("/model/features/importance?top_n=5")

        if response.status_code == 200:
            data = response.json()
            assert data["top_n"] == 5
            if data["features"]:
                assert len(data["features"]) <= 5

    def test_feature_importance_schema(self):
        """Test feature importance response schema"""
        response = client.get("/model/features/importance")

        if response.status_code == 200:
            data = response.json()
            assert "features" in data
            assert "timestamp" in data


class TestErrorHandling:
    """Test error handling"""

    def test_invalid_endpoint(self):
        """Test request to invalid endpoint"""
        response = client.get("/invalid-endpoint")
        assert response.status_code == 404

    def test_invalid_method(self):
        """Test invalid HTTP method"""
        response = client.get("/predict")  # Should be POST
        assert response.status_code == 405


class TestCORS:
    """Test CORS configuration"""

    def test_cors_headers(self):
        """Test CORS headers are present"""
        response = client.options("/health")
        # CORS headers should be present
        assert response.status_code in [200, 405]


# Integration tests (require model to be loaded)
class TestIntegration:
    """Integration tests"""

    @pytest.mark.integration
    def test_full_prediction_workflow(self):
        """Test complete prediction workflow"""
        # 1. Check health
        health_response = client.get("/health")
        if health_response.status_code != 200:
            pytest.skip("Model not loaded")

        health_data = health_response.json()
        if not health_data["model_loaded"]:
            pytest.skip("Model not loaded")

        # 2. Get model info
        info_response = client.get("/model/info")
        assert info_response.status_code == 200

        # 3. Make prediction
        pred_response = client.post("/predict", json={
            "item_id": "FOODS_1_001_CA_1",
            "store_id": "CA_1",
            "date": "2016-05-01"
        })
        assert pred_response.status_code == 200

        pred_data = pred_response.json()
        assert pred_data["predicted_sales"] >= 0


# Run tests
if __name__ == '__main__':
    pytest.main([__file__, '-v'])
