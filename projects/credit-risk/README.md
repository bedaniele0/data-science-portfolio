# Credit Risk Scoring (E2E)

**One-liner:** Sistema de scoring crediticio para estimar probabilidad de default y habilitar decisiones de riesgo vía API y monitoreo.  
**Stack:** Python, pandas, scikit-learn/LightGBM, FastAPI, Streamlit (si aplica), monitoreo de drift (si aplica).  
**Deliverable:** API (FastAPI) + pipeline reproducible + monitoreo (drift/metrics).  
**Results:** AUC 0.7813, KS 0.4251, Recall 0.8704 (threshold 0.12), Brier 0.1349.

## Problem
Construir un modelo de riesgo crediticio que entregue probabilidades confiables (calibradas si aplica) y permita operación segura en un flujo de evaluación de solicitudes.

## Data
- Source: UCI Default of Credit Card Clients (Taiwan)
- Size: 30,000 clientes, 23 features + target

## Approach
- Preparación de datos (missing, outliers) y validación para evitar leakage.
- Entrenamiento y selección por métricas de ranking (AUC/KS) y/o calibración (Brier / reliability).
- Exposición por API y monitoreo: drift de variables + performance por ventanas.

## Results
- Metric(s): AUC 0.7813, KS 0.4251, Recall 0.8704, Precision 0.3107, Brier 0.1349
- Key insight: En riesgo, además de AUC/KS, la calibración y el monitoreo son críticos para decisiones consistentes.

## Demo
- API: local (`uvicorn src.api.main:app --reload`)
- Dashboard/Monitoring: local (`streamlit run src/visualization/dashboard.py`)

## How to run
- Install:
  - `pip install -r requirements.txt`
- Run:
  - `uvicorn src.api.main:app --reload`
  - `streamlit run src/visualization/dashboard.py`

## Repo structure
- `src/` lógica de datos/features/modelo
- `app/` API y/o dashboard
- `tests/` pruebas (si aplica)
- `reports/` figuras y resultados

## Next steps
- Definir política de decisión: umbral por costo + revisión manual.
- Agregar explainability (SHAP) y reportes de estabilidad (PSI/KS por feature).
