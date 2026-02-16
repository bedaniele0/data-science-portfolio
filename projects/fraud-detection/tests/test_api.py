# -*- coding: utf-8 -*-
"""
============================================================================
test_api.py - Test Suite para Fraud Detection API
============================================================================
Tests completos para todos los endpoints de la API

Autor: Ing. Daniel Varela Perez
Email: bedaniele0@gmail.com
Metodologia: DVP-PRO
============================================================================
"""

import pytest
from fastapi.testclient import TestClient
from datetime import timedelta

# Import app
from api.main import app
from api.auth import create_access_token, get_password_hash


# ============================================================================
# TEST CLIENT SETUP
# ============================================================================

@pytest.fixture
def client():
    """Cliente de prueba para la API."""
    return TestClient(app)


@pytest.fixture
def auth_headers():
    """Headers con JWT token válido."""
    access_token = create_access_token(
        data={"sub": "testuser"},
        expires_delta=timedelta(minutes=30)
    )
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def sample_transaction():
    """Transacción de ejemplo para testing."""
    return {
        "Time": 0,
        "V1": -1.3598071336738,
        "V2": -0.0727811733098497,
        "V3": 2.53634673796914,
        "V4": 1.37815522427443,
        "V5": -0.338320769942518,
        "V6": 0.462387777762292,
        "V7": 0.239598554061257,
        "V8": 0.0986979012610507,
        "V9": 0.363786969611213,
        "V10": 0.0907941719789316,
        "V11": -0.551599533260813,
        "V12": -0.617800855762348,
        "V13": -0.991389847235408,
        "V14": -0.311169353699879,
        "V15": 1.46817697209427,
        "V16": -0.470400525259478,
        "V17": 0.207971241929242,
        "V18": 0.0257905801985591,
        "V19": 0.403992960255733,
        "V20": 0.251412098239705,
        "V21": -0.018306777944153,
        "V22": 0.277837575558899,
        "V23": -0.110473910188767,
        "V24": 0.0669280749146731,
        "V25": 0.128539358273528,
        "V26": -0.189114843888824,
        "V27": 0.133558376740387,
        "V28": -0.0210530534538215,
        "Amount": 149.62
    }


# ============================================================================
# ROOT & HEALTH TESTS
# ============================================================================

def test_read_root(client):
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Fraud Detection API"
    assert data["version"] == "1.0.0"
    assert data["status"] == "operational"


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "model_loaded" in data
    assert "model_version" in data
    assert "timestamp" in data


def test_status_endpoint(client):
    """Test status endpoint."""
    response = client.get("/status")
    assert response.status_code == 200
    data = response.json()
    assert "api_version" in data
    assert "model_loaded" in data
    assert "optimal_threshold" in data


# ============================================================================
# AUTHENTICATION TESTS
# ============================================================================

def test_login_success(client):
    """Test successful login."""
    response = client.post(
        "/token",
        data={"username": "admin", "password": "admin123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client):
    """Test login with invalid credentials."""
    response = client.post(
        "/token",
        data={"username": "admin", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]


def test_login_nonexistent_user(client):
    """Test login with non-existent user."""
    response = client.post(
        "/token",
        data={"username": "nonexistent", "password": "password"}
    )
    assert response.status_code == 401


def test_get_current_user(client, auth_headers):
    """Test getting current user info."""
    response = client.get("/users/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "username" in data
    assert "email" in data


def test_get_current_user_unauthorized(client):
    """Test getting current user without authentication."""
    response = client.get("/users/me")
    assert response.status_code == 403  # Forbidden


def test_get_current_user_invalid_token(client):
    """Test getting current user with invalid token."""
    headers = {"Authorization": "Bearer invalid-token"}
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 401


# ============================================================================
# PREDICTION TESTS
# ============================================================================

def test_predict_single_success(client, auth_headers, sample_transaction):
    """Test successful single prediction."""
    response = client.post(
        "/api/v1/predict",
        json=sample_transaction,
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()

    # Verificar estructura de response
    assert "transaction_id" in data
    assert "fraud_probability" in data
    assert "is_fraud" in data
    assert "risk_level" in data
    assert "threshold_used" in data
    assert "model_version" in data
    assert "prediction_timestamp" in data

    # Verificar tipos
    assert isinstance(data["fraud_probability"], float)
    assert isinstance(data["is_fraud"], bool)
    assert 0 <= data["fraud_probability"] <= 1
    assert data["risk_level"] in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]


def test_predict_single_unauthorized(client, sample_transaction):
    """Test prediction without authentication."""
    response = client.post("/api/v1/predict", json=sample_transaction)
    assert response.status_code == 403


def test_predict_single_invalid_data(client, auth_headers):
    """Test prediction with invalid data."""
    invalid_transaction = {"Time": 0, "Amount": -100}  # Missing fields
    response = client.post(
        "/api/v1/predict",
        json=invalid_transaction,
        headers=auth_headers
    )
    assert response.status_code == 422  # Validation error


def test_predict_single_negative_amount(client, auth_headers, sample_transaction):
    """Test prediction with negative amount."""
    sample_transaction["Amount"] = -100
    response = client.post(
        "/api/v1/predict",
        json=sample_transaction,
        headers=auth_headers
    )
    assert response.status_code == 422


def test_predict_batch_success(client, auth_headers, sample_transaction):
    """Test successful batch prediction."""
    batch_request = {
        "transactions": [sample_transaction, sample_transaction]
    }

    response = client.post(
        "/api/v1/predict/batch",
        json=batch_request,
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()

    assert "predictions" in data
    assert "total_transactions" in data
    assert "fraud_count" in data
    assert "fraud_rate" in data
    assert "processing_time" in data

    assert len(data["predictions"]) == 2
    assert data["total_transactions"] == 2
    assert isinstance(data["fraud_rate"], float)
    assert isinstance(data["processing_time"], float)


def test_predict_batch_unauthorized(client, sample_transaction):
    """Test batch prediction without authentication."""
    batch_request = {"transactions": [sample_transaction]}
    response = client.post("/api/v1/predict/batch", json=batch_request)
    assert response.status_code == 403


def test_predict_batch_empty(client, auth_headers):
    """Test batch prediction with empty list."""
    batch_request = {"transactions": []}
    response = client.post(
        "/api/v1/predict/batch",
        json=batch_request,
        headers=auth_headers
    )
    # Could be 200 with empty results or 422 validation error
    assert response.status_code in [200, 422]


def test_predict_batch_max_limit(client, auth_headers, sample_transaction):
    """Test batch prediction at max limit (1000)."""
    batch_request = {
        "transactions": [sample_transaction] * 1000
    }

    response = client.post(
        "/api/v1/predict/batch",
        json=batch_request,
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total_transactions"] == 1000


def test_predict_batch_over_limit(client, auth_headers, sample_transaction):
    """Test batch prediction over limit (>1000)."""
    batch_request = {
        "transactions": [sample_transaction] * 1001
    }

    response = client.post(
        "/api/v1/predict/batch",
        json=batch_request,
        headers=auth_headers
    )
    assert response.status_code == 422  # Validation error


# ============================================================================
# MODEL MANAGEMENT TESTS
# ============================================================================

def test_get_model_info(client):
    """Test getting model information."""
    response = client.get("/api/v1/model/info")
    assert response.status_code == 200
    data = response.json()

    assert "model_type" in data
    assert "model_version" in data
    assert "optimal_threshold" in data
    assert "features_count" in data
    assert "performance_metrics" in data

    assert data["model_type"] == "RandomForestClassifier"
    assert data["features_count"] == 30

    # Verificar métricas
    metrics = data["performance_metrics"]
    assert "precision" in metrics
    assert "recall" in metrics
    assert "f1_score" in metrics
    assert "accuracy" in metrics


def test_update_threshold_success(client, auth_headers):
    """Test successful threshold update."""
    response = client.put(
        "/api/v1/model/threshold?new_threshold=0.6",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()

    assert "message" in data
    assert "old_threshold" in data
    assert "new_threshold" in data
    assert data["new_threshold"] == 0.6

    # Restaurar threshold original
    client.put(
        "/api/v1/model/threshold?new_threshold=0.5",
        headers=auth_headers
    )


def test_update_threshold_unauthorized(client):
    """Test threshold update without authentication."""
    response = client.put("/api/v1/model/threshold?new_threshold=0.6")
    assert response.status_code == 403


def test_update_threshold_invalid_value(client, auth_headers):
    """Test threshold update with invalid value."""
    response = client.put(
        "/api/v1/model/threshold?new_threshold=1.5",
        headers=auth_headers
    )
    assert response.status_code == 422  # Validation error

    response = client.put(
        "/api/v1/model/threshold?new_threshold=-0.1",
        headers=auth_headers
    )
    assert response.status_code == 422


# ============================================================================
# MONITORING TESTS
# ============================================================================

def test_get_metrics(client):
    """Test getting monitoring metrics."""
    response = client.get("/api/v1/monitoring/metrics")
    assert response.status_code == 200
    data = response.json()

    assert "model_loaded" in data
    assert "model_version" in data
    assert "threshold" in data
    assert "timestamp" in data


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

def test_full_workflow(client, sample_transaction):
    """Test complete workflow: login -> predict -> check status."""
    # 1. Login
    login_response = client.post(
        "/token",
        data={"username": "admin", "password": "admin123"}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Get user info
    user_response = client.get("/users/me", headers=headers)
    assert user_response.status_code == 200

    # 3. Make prediction
    pred_response = client.post(
        "/api/v1/predict",
        json=sample_transaction,
        headers=headers
    )
    assert pred_response.status_code == 200

    # 4. Check model info
    info_response = client.get("/api/v1/model/info")
    assert info_response.status_code == 200

    # 5. Get metrics
    metrics_response = client.get("/api/v1/monitoring/metrics")
    assert metrics_response.status_code == 200


def test_authentication_required_endpoints(client, sample_transaction):
    """Test that protected endpoints require authentication."""
    protected_endpoints = [
        ("GET", "/users/me"),
        ("POST", "/api/v1/predict", sample_transaction),
        ("POST", "/api/v1/predict/batch", {"transactions": [sample_transaction]}),
        ("PUT", "/api/v1/model/threshold?new_threshold=0.6", None),
    ]

    for method, endpoint, *json_data in protected_endpoints:
        if method == "GET":
            response = client.get(endpoint)
        elif method == "POST":
            response = client.post(endpoint, json=json_data[0] if json_data else None)
        elif method == "PUT":
            response = client.put(endpoint)

        # Should be 403 (Forbidden) or 401 (Unauthorized)
        assert response.status_code in [401, 403], f"Endpoint {endpoint} should require auth"


# ============================================================================
# PERFORMANCE TESTS
# ============================================================================

def test_prediction_performance(client, auth_headers, sample_transaction):
    """Test prediction response time."""
    import time

    start = time.time()
    response = client.post(
        "/api/v1/predict",
        json=sample_transaction,
        headers=auth_headers
    )
    elapsed = time.time() - start

    assert response.status_code == 200
    assert elapsed < 1.0  # Should respond in less than 1 second


def test_batch_prediction_performance(client, auth_headers, sample_transaction):
    """Test batch prediction performance."""
    import time

    batch_request = {
        "transactions": [sample_transaction] * 100
    }

    start = time.perf_counter()
    response = client.post(
        "/api/v1/predict/batch",
        json=batch_request,
        headers=auth_headers
    )
    elapsed = time.perf_counter() - start

    assert response.status_code == 200
    # Allow small variance across environments (local vs CI).
    assert elapsed < 7.0  # Should complete 100 predictions in less than 7 seconds

    data = response.json()
    assert data["total_transactions"] == 100


# ============================================================================
# ERROR HANDLING TESTS
# ============================================================================

def test_404_endpoint(client):
    """Test non-existent endpoint."""
    response = client.get("/nonexistent")
    assert response.status_code == 404


def test_method_not_allowed(client):
    """Test wrong HTTP method."""
    response = client.post("/health")  # GET endpoint
    assert response.status_code == 405


# ============================================================================
# PYTEST MARKERS
# ============================================================================

# Run with: pytest -m api
# Run with: pytest -m auth
# Run with: pytest -m predictions

pytestmark = pytest.mark.api
