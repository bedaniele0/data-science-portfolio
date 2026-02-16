# Walmart Demand Forecasting API - Documentation

**Author**: Ing. Daniel Varela Perez
**Email**: bedaniele0@gmail.com
**Tel**: +52 55 4189 3428
**Date**: December 5, 2024
**Version**: 1.0.0

---

## Overview

RESTful API for forecasting daily sales across Walmart stores using a trained LightGBM model.

**Base URL**: `http://localhost:8000`
**Interactive Docs**: `http://localhost:8000/docs`
**ReDoc**: `http://localhost:8000/redoc`

---

## Quick Start

### Start the API

```bash
# Using Docker Compose (recommended)
docker-compose up -d

# Or using Uvicorn directly
uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```

### Test the API

```bash
# Health check
curl http://localhost:8000/health

# Make a prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "item_id": "FOODS_1_001_CA_1",
    "store_id": "CA_1",
    "date": "2016-05-01"
  }'
```

---

## Endpoints

### 1. Root Endpoint

**GET /**

Get API information

**Response:**
```json
{
  "message": "Walmart Demand Forecasting API",
  "version": "1.0.0",
  "docs": "/docs",
  "health": "/health",
  "model_info": "/model/info"
}
```

---

### 2. Health Check

**GET /health**

Check API health and model status

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_version": "1.0.0",
  "uptime_seconds": 3600.5,
  "timestamp": "2024-12-05T15:30:00Z"
}
```

**Status Codes:**
- `200 OK`: Service healthy
- `503 Service Unavailable`: Model not loaded

---

### 3. Model Information

**GET /model/info**

Get detailed model information

**Response:**
```json
{
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
```

**Status Codes:**
- `200 OK`: Success
- `503 Service Unavailable`: Model not loaded

---

### 4. Single Prediction

**POST /predict**

Predict daily sales for a single item-store-date combination

**Request Body:**
```json
{
  "item_id": "FOODS_1_001_CA_1",
  "store_id": "CA_1",
  "date": "2016-05-01",
  "features": {
    "feature_0": 1.5,
    "feature_1": 2.3
  }
}
```

**Parameters:**
- `item_id` (required): Product-store identifier
- `store_id` (required): Store identifier
- `date` (required): Prediction date (YYYY-MM-DD)
- `features` (optional): Pre-computed features dictionary

**Response:**
```json
{
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
```

**Status Codes:**
- `200 OK`: Prediction successful
- `400 Bad Request`: Invalid input
- `422 Unprocessable Entity`: Validation error
- `503 Service Unavailable`: Model not loaded

**Example with curl:**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "item_id": "FOODS_1_001_CA_1",
    "store_id": "CA_1",
    "date": "2016-05-01"
  }'
```

**Example with Python:**
```python
import requests

url = "http://localhost:8000/predict"
data = {
    "item_id": "FOODS_1_001_CA_1",
    "store_id": "CA_1",
    "date": "2016-05-01"
}

response = requests.post(url, json=data)
prediction = response.json()
print(f"Predicted sales: {prediction['predicted_sales']}")
```

---

### 5. Batch Predictions

**POST /predict/batch**

Predict daily sales for multiple items

**Request Body:**
```json
{
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
```

**Parameters:**
- `items` (required): Array of prediction requests (max 1000)

**Response:**
```json
{
  "predictions": [
    {
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
  ],
  "total_items": 1,
  "processing_time_ms": 45.2
}
```

**Status Codes:**
- `200 OK`: Predictions successful
- `400 Bad Request`: Invalid input
- `422 Unprocessable Entity`: Validation error
- `503 Service Unavailable`: Model not loaded

**Example with curl:**
```bash
curl -X POST http://localhost:8000/predict/batch \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {"item_id": "FOODS_1_001_CA_1", "store_id": "CA_1", "date": "2016-05-01"},
      {"item_id": "FOODS_1_002_CA_1", "store_id": "CA_1", "date": "2016-05-01"}
    ]
  }'
```

---

### 6. Feature Importance

**GET /model/features/importance**

Get top feature importances from the model

**Query Parameters:**
- `top_n` (optional): Number of top features to return (default: 10)

**Response:**
```json
{
  "top_n": 10,
  "features": [
    {
      "feature": "sales_rolling_mean_7",
      "importance": 509.0
    },
    {
      "feature": "sales_lag_3",
      "importance": 292.0
    }
  ],
  "timestamp": "2024-12-05T15:30:00Z"
}
```

**Status Codes:**
- `200 OK`: Success
- `503 Service Unavailable`: Model not loaded

**Example:**
```bash
curl http://localhost:8000/model/features/importance?top_n=5
```

---

## Error Responses

All errors follow this schema:

```json
{
  "error": "ErrorType",
  "message": "Human-readable error message",
  "detail": "Detailed error information",
  "timestamp": "2024-12-05T15:30:00Z"
}
```

**Common Error Codes:**
- `400 Bad Request`: Invalid input data
- `404 Not Found`: Endpoint not found
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error
- `503 Service Unavailable`: Service unavailable (model not loaded)

---

## Rate Limiting

**Current**: No rate limiting implemented

**Recommended for production**:
- 100 requests/minute per IP for single predictions
- 10 requests/minute per IP for batch predictions
- 1000 items max per batch request

---

## Authentication

**Current**: No authentication required

**Recommended for production**:
- API Key authentication
- JWT tokens for user-specific requests
- OAuth2 for third-party integrations

---

## Performance

**Latency:**
- Single prediction: ~50ms
- Batch prediction (100 items): ~2s

**Throughput:**
- ~1000 predictions/second (single endpoint)
- ~5000 predictions/second (batch endpoint)

**Resource Usage:**
- Memory: ~500 MB
- CPU: 1-2 cores recommended

---

## Model Updates

To update the model without downtime:

1. Place new model file in `models/` directory
2. Update model version in code
3. Restart API: `docker-compose restart api`

Or use rolling updates with Kubernetes:
```bash
kubectl rollout restart deployment walmart-forecasting-api
```

---

## Monitoring

**Health Check:**
```bash
# Check every 30 seconds
watch -n 30 'curl -s http://localhost:8000/health | jq'
```

**Logs:**
```bash
# View logs
docker-compose logs -f api

# Or with Docker
docker logs -f walmart-forecasting-api
```

**Metrics to Monitor:**
- Request rate (requests/second)
- Response time (p50, p95, p99)
- Error rate (%)
- Model prediction time
- Memory usage
- CPU usage

---

## Development

### Run locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run with auto-reload
uvicorn src.api.main:app --reload --port 8000
```

### Run tests

```bash
# Run API tests
pytest tests/test_api.py -v

# Run with coverage
pytest tests/ --cov=src.api
```

### Interactive API docs

Visit `http://localhost:8000/docs` for interactive Swagger UI

---

## Troubleshooting

### Model not loading

**Symptom**: `/health` returns `model_loaded: false`

**Solution**:
1. Check model file exists: `ls models/lightgbm_model.pkl`
2. Check file permissions
3. Check logs: `docker-compose logs api`

### High latency

**Solution**:
1. Use batch endpoint for multiple predictions
2. Increase container resources
3. Enable response caching
4. Use load balancer for horizontal scaling

### Memory issues

**Solution**:
1. Increase Docker memory limit in `docker-compose.yml`
2. Reduce batch size
3. Monitor with: `docker stats walmart-forecasting-api`

---

## Security Best Practices

1. **Use HTTPS** in production
2. **Enable authentication** (API keys, JWT)
3. **Rate limiting** to prevent abuse
4. **Input validation** (already implemented with Pydantic)
5. **Run as non-root user** (already configured in Dockerfile)
6. **Keep dependencies updated**: `pip install -U -r requirements.txt`
7. **Monitor logs** for suspicious activity

---

## API Clients

### Python Client Example

```python
import requests

class WalmartForecastingClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url

    def health_check(self):
        return requests.get(f"{self.base_url}/health").json()

    def predict(self, item_id, store_id, date):
        data = {
            "item_id": item_id,
            "store_id": store_id,
            "date": date
        }
        return requests.post(f"{self.base_url}/predict", json=data).json()

    def predict_batch(self, items):
        data = {"items": items}
        return requests.post(f"{self.base_url}/predict/batch", json=data).json()

# Usage
client = WalmartForecastingClient()
result = client.predict("FOODS_1_001_CA_1", "CA_1", "2016-05-01")
print(result["predicted_sales"])
```

---

## Support

For issues, questions, or feature requests:

**Author**: Ing. Daniel Varela Perez
**Email**: bedaniele0@gmail.com
**Phone**: +52 55 4189 3428

---

**Last Updated**: December 5, 2024
**API Version**: 1.0.0
**Model Version**: 1.0.0
