# Diseño Arquitectónico - Fraud Detection (DVP-PRO Fase 2)
Autor: Ing. Daniel Varela Perez  
Email: bedaniele0@gmail.com  
Tel: +52 55 4189 3428

## 1. Vista de Alto Nivel (flujo E2E)
```
Datos brutos (raw CSV/Parquet) ─┐
                               │
                      [ETL/FE CLI: fraud-train]
                               │
                     data/processed/*.parquet
                               │
                 Entrenamiento (RandomForest, threshold tuning)
                               │
                     models/*.pkl + metrics.json
                               │
        ┌───────────────┬──────────────────────┬───────────────────┐
        │                │                      │                   │
   API FastAPI     Dashboard Streamlit    Jobs Batch/CLI      Monitoreo (Prom/Grafana)
  /api/v1/predict   fraud-dashboard       fraud-predict        /api/v1/monitoring/metrics
```

## 2. Componentes
- Ingesta/ETL: scripts CLI (`fraud-train`, `fraud-evaluate`, `fraud-predict`) leen `data/processed/*.parquet`.
- Feature Engineering: normalización de columnas, derivadas (amount_log, hour_from_start, ratios).
- Modelo: RandomForest clasificador con threshold ajustable, artefactos en `models/`.
- Serving: FastAPI (`api/main.py`) con auth (JWT/API key), endpoints predict individuales y batch.
- Visualización: Streamlit (`dashboard/fraud_detection_dashboard.py`) consume API y permite carga de CSV.
- Monitoreo: Prometheus/Grafana vía `docker-compose.monitoring.yml`; métricas expuestas por API.

## 3. Contratos de Datos (entradas modelo/API)
- Esquema mínimo requerido por modelo (float):
  - `Time`, `Amount`, `V1` ... `V28`
- Reglas:
  - Sin nulos; imputación previa en ETL.
  - Normalización de nombres: variantes mapeadas a nombres estándar (ej. `Tiempo` -> `Time`).
  - Batch API: máximo 1000 filas por request; archivos CSV con header.
- Validaciones:
  - Tipos numéricos; filas inválidas se rechazan con 400.
  - Versionamiento: `models/threshold_config.json` debe acompañar al `.pkl`.

## 4. Contratos de Servicio (API)
- `POST /api/v1/predict`
  - Request: JSON con campos `Time`, `Amount`, `V1`...`V28` (floats).
  - Response:
    ```json
    {
      "fraud_probability": 0.12,
      "is_fraud": false,
      "threshold": 0.300,
      "model_version": "1.0.0"
    }
    ```
- `POST /api/v1/predict/batch`
  - Request: file CSV (<=1000 filas) o JSON list de objetos.
  - Response: lista de predicciones + métricas agregadas.
- `GET /api/v1/model/info`: metadatos (features esperadas, threshold, fecha de entrenamiento).
- `PUT /api/v1/model/threshold?new_threshold=0.35`: actualiza umbral (solo rol admin).
- `GET /api/v1/monitoring/metrics`: expone métricas para Prometheus.
- Seguridad: JWT / API Key; HTTPS recomendado en despliegue.

## 5. Datos y Artefactos
- Datos procesados: `data/processed/train_clean.parquet`, `validation_clean.parquet`, `test_clean.parquet`.
- Modelos: `models/improved_recall_threshold_model.pkl`, `models/simple_fraud_model.pkl`, `models/threshold_config.json`.
- Config: `config/alerts_config.yaml` (alertas), `configs/` (parámetros ML/serving si aplica).

## 6. Despliegue y Operación
- Local/dev: `fraud-api` (uvicorn) + `fraud-dashboard` (streamlit).
- Contenedor: `Dockerfile` (API) + `docker-compose.monitoring.yml` (Prom/Grafana).
- Variables de entorno clave:
  - `MODEL_PATH`, `PREPROCESSOR_PATH`, `THRESHOLD`, `API_KEYS`, `JWT_SECRET`, `LOG_LEVEL`.
  - Monitoreo: `PROMETHEUS_PORT`, `GRAFANA_ADMIN_PASSWORD`.
- Puertos: API 8000, Dashboard 8501, Prometheus 9090, Grafana 3000.

## 7. Monitoreo y Alertas
- Métricas expuestas: latencia de predicción, conteo de solicitudes, tasa de fraude estimada, drift (si está habilitado en `src/monitoring/`).
- Alertas: reglas ejemplo en `config/grafana/alert_rules.yml`; alertas de tasa de fraude alta y PSI/KS.
- Logs: estructurados (JSON) sin PII; rotación recomendada.

## 8. ADR / Decisiones Clave (resumen)
- Algoritmo: RandomForest por desempeño en tabular desbalanceado y robustez ante ruido.
- Threshold dinámico: configurable vía API para ajustar recall/FPR según negocio.
- Seguridad: JWT/API key con hashing bcrypt (api/auth.py).
- Observabilidad: Prometheus/Grafana de referencia; apto para migrar a stack gestionado.

## 9. Checklist de Arquitectura (DoD F2)
- [x] Contratos de datos y servicios documentados.
- [x] Flujos ETL→ML→Serving→Monitoreo descritos.
- [x] Variables de entorno y puertos definidos.
- [ ] Diagrama formal (C4) incorporado en docs (pendiente si se requiere para compliance).
- [ ] Pruebas de carga para validar SLA de latencia/throughput documentadas.
