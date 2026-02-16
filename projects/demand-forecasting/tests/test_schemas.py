"""
Unit tests for API schemas defined in src/api/schemas.py

Author: Ing. Daniel Varela Perez
Email: bedaniele0@gmail.com
Date: December 15, 2025
"""

import pytest
from pydantic import ValidationError
from datetime import datetime

from src.api.schemas import (
    PredictionRequest,
    BatchPredictionRequest,
    PredictionResponse,
    BatchPredictionResponse,
    HealthResponse,
    ModelInfoResponse,
    ErrorResponse
)


class TestPredictionRequest:
    """Tests for the PredictionRequest schema."""

    def test_success_with_valid_data(self):
        """Test successful validation with correct and complete data."""
        data = {
            "item_id": "FOODS_1_001_CA_1",
            "store_id": "CA_1",
            "date": "2025-12-15"
        }
        try:
            req = PredictionRequest(**data)
            assert req.item_id == data["item_id"]
            assert req.store_id == data["store_id"]
            assert req.date == data["date"]
            assert req.features is None
        except ValidationError as e:
            pytest.fail(f"Validation failed unexpectedly: {e}")

    def test_success_with_optional_features(self):
        """Test successful validation when optional features are provided."""
        data = {
            "item_id": "FOODS_1_001_CA_1",
            "store_id": "CA_1",
            "date": "2025-12-15",
            "features": {"price": 2.5, "day_of_week": 1}
        }
        req = PredictionRequest(**data)
        assert req.features["price"] == 2.5

    def test_fail_on_missing_required_field(self):
        """Test that ValidationError is raised if a required field is missing."""
        with pytest.raises(ValidationError) as excinfo:
            PredictionRequest(item_id="FOODS_1_001_CA_1", date="2025-12-15")
        assert "store_id" in str(excinfo.value)

    def test_fail_on_invalid_date_format(self):
        """Test the custom date validator fails on incorrect date formats."""
        data = {
            "item_id": "FOODS_1_001_CA_1",
            "store_id": "CA_1",
            "date": "15-12-2025"  # Invalid format
        }
        with pytest.raises(ValidationError) as excinfo:
            PredictionRequest(**data)
        assert "Date must be in YYYY-MM-DD format" in str(excinfo.value)

    def test_fail_on_non_string_date(self):
        """Test that a non-string date also fails validation."""
        data = {
            "item_id": "FOODS_1_001_CA_1",
            "store_id": "CA_1",
            "date": 12345
        }
        with pytest.raises(ValidationError):
            PredictionRequest(**data)


class TestBatchPredictionRequest:
    """Tests for the BatchPredictionRequest schema."""

    def test_success_with_valid_list(self):
        """Test successful validation with a list of valid items."""
        data = {
            "items": [
                {"item_id": "item_1", "store_id": "store_A", "date": "2025-01-01"},
                {"item_id": "item_2", "store_id": "store_B", "date": "2025-01-02"},
            ]
        }
        batch_req = BatchPredictionRequest(**data)
        assert len(batch_req.items) == 2
        assert batch_req.items[0].item_id == "item_1"

    def test_fail_on_empty_list(self):
        """Test failure when the items list is empty (violates min_length)."""
        with pytest.raises(ValidationError) as excinfo:
            BatchPredictionRequest(items=[])
        assert "List should have at least 1 item" in str(excinfo.value)

    def test_fail_on_list_too_long(self):
        """Test failure when the items list is too long (violates max_length)."""
        long_list = [{"item_id": f"item_{i}", "store_id": "store_A", "date": "2025-01-01"} for i in range(1001)]
        with pytest.raises(ValidationError) as excinfo:
            BatchPredictionRequest(items=long_list)
        assert "List should have at most 1000 items" in str(excinfo.value)

    def test_fail_if_any_item_is_invalid(self):
        """Test failure if one of the items in the list is invalid."""
        data = {
            "items": [
                {"item_id": "item_1", "store_id": "store_A", "date": "2025-01-01"},
                {"item_id": "item_2", "date": "2025-01-02"},  # Missing store_id
            ]
        }
        with pytest.raises(ValidationError):
            BatchPredictionRequest(**data)


class TestResponseSchemas:
    """High-level tests for response schemas to ensure they validate correct data."""

    def test_prediction_response_success(self):
        """Test PredictionResponse validates a typical valid payload."""
        data = {
            "item_id": "item_1",
            "store_id": "store_A",
            "date": "2025-01-01",
            "predicted_sales": 10.5,
            "prediction_interval": {"lower": 8.0, "upper": 12.0},
            "model_version": "1.0.0",
            "timestamp": datetime.now().isoformat()
        }
        try:
            PredictionResponse(**data)
        except ValidationError as e:
            pytest.fail(f"PredictionResponse failed validation: {e}")

    def test_batch_prediction_response_success(self):
        """Test BatchPredictionResponse validates a typical valid payload."""
        pred_data = {
            "item_id": "item_1", "store_id": "store_A", "date": "2025-01-01",
            "predicted_sales": 10.5, "model_version": "1.0.0", "timestamp": datetime.now().isoformat()
        }
        batch_data = {
            "predictions": [pred_data],
            "total_items": 1,
            "processing_time_ms": 50.1
        }
        try:
            BatchPredictionResponse(**batch_data)
        except ValidationError as e:
            pytest.fail(f"BatchPredictionResponse failed validation: {e}")

    def test_health_response_success(self):
        """Test HealthResponse validates a typical valid payload."""
        data = {
            "status": "healthy",
            "model_loaded": True,
            "model_version": "1.0.0",
            "uptime_seconds": 1234.5,
            "timestamp": datetime.now().isoformat()
        }
        try:
            HealthResponse(**data)
        except ValidationError as e:
            pytest.fail(f"HealthResponse failed validation: {e}")

    def test_model_info_response_success(self):
        """Test ModelInfoResponse validates a typical valid payload."""
        data = {
            "model_name": "Test Model",
            "model_version": "1.0.0",
            "model_type": "LGBM",
            "training_date": "2025-12-01",
            "features_count": 93,
            "performance_metrics": {"mae": 0.75}
        }
        try:
            ModelInfoResponse(**data)
        except ValidationError as e:
            pytest.fail(f"ModelInfoResponse failed validation: {e}")

    def test_error_response_success(self):
        """Test ErrorResponse validates a typical valid payload."""
        data = {
            "error": "Internal Server Error",
            "message": "Something went wrong.",
            "detail": "Traceback here",
            "timestamp": datetime.now().isoformat()
        }
        try:
            ErrorResponse(**data)
        except ValidationError as e:
            pytest.fail(f"ErrorResponse failed validation: {e}")
