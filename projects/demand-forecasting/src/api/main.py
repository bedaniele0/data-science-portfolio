"""
FastAPI para Walmart Demand Forecasting

Contrato alineado a DVP-PRO y a la suite de pruebas:
- version 1.0.0
- health con estado del modelo
- endpoints /model/info, /model/features/importance y /predict/batch
"""

import logging
import time
from datetime import date as dt_date, datetime as dt_datetime
from typing import Any, Dict, List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .model_service import get_model_service

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

APP_VERSION = "1.0.0"
start_time = time.time()

app = FastAPI(
    title="Walmart Demand Forecasting API",
    version=APP_VERSION,
    description="API para predicción de demanda de Walmart usando LightGBM",
)


# ==============================
#   Esquemas de entrada/salida
# ==============================


class PredictRequest(BaseModel):
    item_id: str = Field(..., example="FOODS_1_003")
    store_id: str = Field(..., example="TX_3")
    date: dt_date = Field(
        ...,
        example="2016-05-23",
        description="Fecha en formato YYYY-MM-DD (debe existir en los datos procesados)",
    )


class PredictResponse(BaseModel):
    item_id: str
    store_id: str
    date: dt_date
    predicted_sales: float
    model_version: str
    timestamp: dt_datetime


class BatchPredictRequest(BaseModel):
    items: List[PredictRequest] = Field(..., min_items=1)


class BatchPredictResponse(BaseModel):
    predictions: List[PredictResponse]
    total_items: int
    processing_time_ms: float


class FeatureImportanceResponse(BaseModel):
    features: List[Dict[str, Any]]
    top_n: int
    timestamp: dt_datetime


# ==============================
#   Eventos de la app
# ==============================


@app.on_event("startup")
def startup_event() -> None:
    """Carga el modelo al iniciar y registra información básica."""
    try:
        svc = get_model_service()
        info = svc.model_info()
        logger.info("Model loaded successfully")
        logger.info("Model info: %s", info)
    except Exception as exc:  # noqa: BLE001
        logger.warning("Model could not be loaded on startup: %s", exc)


# ==============================
#   Endpoints
# ==============================


@app.get("/")
def root() -> Dict[str, Any]:
    return {
        "message": "Walmart Demand Forecasting API",
        "status": "ok",
        "version": APP_VERSION,
    }


@app.get("/health")
def health() -> Dict[str, Any]:
    """Reporte de salud con tiempo de vida y estado del modelo."""
    detail = "ok"
    try:
        svc = get_model_service()
        model_info = svc.model_info()
        model_ready, detail = svc.is_ready()
        model_version = model_info.get("model_version", APP_VERSION)
    except Exception as exc:  # noqa: BLE001
        logger.warning("Health check: model not loaded (%s)", exc)
        model_ready = False
        model_version = APP_VERSION
        detail = str(exc)

    return {
        "status": "healthy" if model_ready else "degraded",
        "model_loaded": model_ready,
        "model_version": model_version,
        "uptime_seconds": round(time.time() - start_time, 2),
        "timestamp": dt_datetime.utcnow().isoformat(),
        "detail": detail if not model_ready else "ok",
    }


@app.get("/model/info")
def model_info() -> Dict[str, Any]:
    svc = get_model_service()
    try:
        return svc.model_info()
    except Exception as exc:  # noqa: BLE001
        logger.error("Model info unavailable: %s", exc)
        raise HTTPException(status_code=503, detail="Model not available")


@app.get("/model/features/importance", response_model=FeatureImportanceResponse)
def feature_importance(top_n: int = 10) -> FeatureImportanceResponse:
    svc = get_model_service()
    try:
        features = svc.feature_importance(top_n=top_n)
    except Exception as exc:  # noqa: BLE001
        logger.error("Feature importance unavailable: %s", exc)
        raise HTTPException(status_code=503, detail="Model not available")

    return FeatureImportanceResponse(
        features=features,
        top_n=top_n,
        timestamp=dt_datetime.utcnow(),
    )


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest) -> PredictResponse:
    """
    Endpoint principal de predicción.

    IMPORTANTE:
    - La (item_id, store_id, date) debe existir en los datos procesados
      (sales_with_features.parquet o valid_data.parquet).
    """
    svc = get_model_service()

    try:
        y_hat = svc.predict_from_request(
            item_id=request.item_id,
            store_id=request.store_id,
            date=request.date,
        )
    except ValueError as e:
        logger.error("Prediction failed: %s", e)
        # Degradamos a 503 para alinearnos con los tests cuando el modelo/datos no están listos
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:  # noqa: BLE001
        logger.exception("Prediction failed with unexpected error")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")

    return PredictResponse(
        item_id=request.item_id,
        store_id=request.store_id,
        date=request.date,
        predicted_sales=y_hat,
        model_version=APP_VERSION,
        timestamp=dt_datetime.utcnow(),
    )


@app.post("/predict/batch", response_model=BatchPredictResponse)
def predict_batch(request: BatchPredictRequest) -> BatchPredictResponse:
    """Predicción batch de múltiples items."""
    svc = get_model_service()
    start = time.time()
    predictions: List[PredictResponse] = []

    for item in request.items:
        try:
            y_hat = svc.predict_from_request(
                item_id=item.item_id,
                store_id=item.store_id,
                date=item.date,
            )
            predictions.append(
                PredictResponse(
                    item_id=item.item_id,
                    store_id=item.store_id,
                    date=item.date,
                    predicted_sales=y_hat,
                    model_version=APP_VERSION,
                    timestamp=dt_datetime.utcnow(),
                )
            )
        except ValueError as exc:
            logger.error("Batch prediction failed for %s: %s", item.item_id, exc)
            raise HTTPException(status_code=503, detail=str(exc))
        except Exception as exc:  # noqa: BLE001
            logger.exception("Batch prediction unexpected error")
            raise HTTPException(status_code=500, detail=str(exc))

    elapsed = (time.time() - start) * 1000

    return BatchPredictResponse(
        predictions=predictions,
        total_items=len(predictions),
        processing_time_ms=round(elapsed, 3),
    )


@app.get("/info")
def info() -> Dict[str, Any]:
    """Alias legacy del endpoint de información."""
    return model_info()
