"""
Pydantic schemas for API request/response validation

Author: Ing. Daniel Varela Perez
Email: bedaniele0@gmail.com
Date: December 5, 2024
"""

from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Any
from datetime import datetime


class PredictionRequest(BaseModel):
    """Request schema for single item prediction"""

    item_id: str = Field(..., description="Item ID (e.g., FOODS_1_001_CA_1)")
    store_id: str = Field(..., description="Store ID (e.g., CA_1)")
    date: str = Field(..., description="Date for prediction (YYYY-MM-DD)")
    features: Optional[Dict[str, float]] = Field(
        None,
        description="Optional pre-computed features. If not provided, will be computed automatically."
    )

    @field_validator('date')
    @classmethod
    def validate_date(cls, v):
        """Validate date format"""
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')

    class Config:
        json_schema_extra = {
            "example": {
                "item_id": "FOODS_1_001_CA_1",
                "store_id": "CA_1",
                "date": "2016-05-01"
            }
        }


class BatchPredictionRequest(BaseModel):
    """Request schema for batch predictions"""

    items: List[PredictionRequest] = Field(
        ...,
        description="List of items to predict",
        min_length=1,
        max_length=1000
    )

    class Config:
        json_schema_extra = {
            "example": {
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
        }


class PredictionResponse(BaseModel):
    """Response schema for single prediction"""

    item_id: str = Field(..., description="Item ID")
    store_id: str = Field(..., description="Store ID")
    date: str = Field(..., description="Prediction date")
    predicted_sales: float = Field(..., description="Predicted sales quantity")
    prediction_interval: Optional[Dict[str, float]] = Field(
        None,
        description="95% prediction interval (lower, upper)"
    )
    model_version: str = Field(..., description="Model version used")
    timestamp: str = Field(..., description="Prediction timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "item_id": "FOODS_1_001_CA_1",
                "store_id": "CA_1",
                "date": "2016-05-01",
                "predicted_sales": 3.45,
                "prediction_interval": {
                    "lower": 2.10,
                    "upper": 4.80
                },
                "model_version": "1.0.0",
                "timestamp": "2024-12-05T15:30:00Z"
            }
        }


class BatchPredictionResponse(BaseModel):
    """Response schema for batch predictions"""

    predictions: List[PredictionResponse] = Field(..., description="List of predictions")
    total_items: int = Field(..., description="Total items predicted")
    processing_time_ms: float = Field(..., description="Total processing time in milliseconds")

    class Config:
        json_schema_extra = {
            "example": {
                "predictions": [
                    {
                        "item_id": "FOODS_1_001_CA_1",
                        "store_id": "CA_1",
                        "date": "2016-05-01",
                        "predicted_sales": 3.45,
                        "model_version": "1.0.0",
                        "timestamp": "2024-12-05T15:30:00Z"
                    }
                ],
                "total_items": 1,
                "processing_time_ms": 45.2
            }
        }


class HealthResponse(BaseModel):
    """Health check response"""

    status: str = Field(..., description="Service status")
    model_loaded: bool = Field(..., description="Whether model is loaded")
    model_version: str = Field(..., description="Model version")
    uptime_seconds: float = Field(..., description="Service uptime in seconds")
    timestamp: str = Field(..., description="Current timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "model_loaded": True,
                "model_version": "1.0.0",
                "uptime_seconds": 3600.5,
                "timestamp": "2024-12-05T15:30:00Z"
            }
        }


class ModelInfoResponse(BaseModel):
    """Model information response"""

    model_name: str = Field(..., description="Model name")
    model_version: str = Field(..., description="Model version")
    model_type: str = Field(..., description="Model type")
    training_date: str = Field(..., description="Model training date")
    features_count: int = Field(..., description="Number of features")
    performance_metrics: Dict[str, float] = Field(..., description="Model performance metrics")

    class Config:
        json_schema_extra = {
            "example": {
                "model_name": "Walmart Demand Forecasting LightGBM",
                "model_version": "1.0.0",
                "model_type": "LightGBM",
                "training_date": "2024-12-05",
                "features_count": 80,
                "performance_metrics": {
                    "mae": 0.6845,
                    "rmse": 3.9554,
                    "mape": 52.75
                }
            }
        }


class ErrorResponse(BaseModel):
    """Error response schema"""

    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    timestamp: str = Field(..., description="Error timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "error": "ValidationError",
                "message": "Invalid input data",
                "detail": "Date must be in YYYY-MM-DD format",
                "timestamp": "2024-12-05T15:30:00Z"
            }
        }
