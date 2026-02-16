# Runbook Operativo - Credit Risk Scoring

**Proyecto:** Credit Risk Scoring (UCI Taiwan)  
**Fase:** F7 - Deployment/Handoff  
**Autor:** Ing. Daniel Varela Perez  
**Fecha:** 2026-02-04

---

## 1. Objetivo
Operación diaria del servicio de scoring, monitoreo básico y procedimientos de contingencia.

## 2. Servicios y Endpoints
- API: `uvicorn src.api.main:app --host 0.0.0.0 --port 8000`
- Health: `GET /health`
- Predicción: `POST /predict`, `POST /predict/batch`
- Métricas: `GET /metrics`

## 3. Checks de Salud
1. `curl http://localhost:8000/health` → `model_loaded: true`
2. `curl http://localhost:8000/model/info` → versión y features correctas
3. `curl http://localhost:8000/metrics` → AUC/KS/threshold disponibles

## 4. Logs
- App: `logs/app.log` (si aplica)
- Training: `logs/train_credit.log`

## 5. Incidentes comunes
- **Modelo no encontrado:** verificar `models/final_model.joblib`
- **Features mismatch:** validar `models/feature_names.json`
- **Puerto ocupado:** cambiar puerto o liberar proceso

## 6. Backups/Artefactos críticos
- `models/final_model.joblib`
- `models/model_metadata.json`
- `models/feature_names.json`
- `reports/metrics/validation_results.json`

---

**© 2026 - DVP-MASTER Framework - Ing. Daniel Varela Perez**
