# Runbook Operativo (F7)

**Proyecto**: Walmart Demand Forecasting & Inventory Optimization  
**Fecha**: 2026-02-06  

## 1. Objetivo

Guía operativa para ejecutar, diagnosticar y recuperar el servicio de forecasting en entorno local/demo.

## 2. Servicios

- **API FastAPI**: `src/api/`
- **Dashboard**: Streamlit (si aplica en tu entorno)

## 3. Comandos básicos

- Levantar API local: `uvicorn src.api.main:app --reload`
- Docker: `docker-compose up --build`

## 4. Salud y diagnóstico

- `GET /health` para estado básico.
- Revisar logs en `logs/` y `docker-compose logs`.

## 5. Incidentes comunes

- **Error de features**: revisar `data/processed/sales_with_features.parquet`.
- **Error de modelo**: verificar `models/lightgbm_model.pkl`.
- **Latencia alta**: validar tamaño de features en memoria.

## 6. Backups

- Modelos: `models/`
- Features: `data/processed/`
