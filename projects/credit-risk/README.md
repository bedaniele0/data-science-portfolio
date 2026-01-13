# Credit Risk Scoring (E2E)

**One-liner:** Sistema de scoring crediticio para estimar probabilidad de default y habilitar decisiones de riesgo vía API y monitoreo.  
**Stack:** Python, pandas, scikit-learn/LightGBM, FastAPI, Streamlit (si aplica), monitoreo de drift (si aplica).  
**Deliverable:** API (FastAPI) + pipeline reproducible + monitoreo (drift/metrics).  
**Results:** <completa: AUC / KS / Brier / otra métrica clave del proyecto>.

## Problem
Construir un modelo de riesgo crediticio que entregue probabilidades confiables (calibradas si aplica) y permita operación segura en un flujo de evaluación de solicitudes.

## Data
- Source: <completa: Kaggle / público / otro>
- Size: <completa: filas/columnas>

## Approach
- Preparación de datos (missing, outliers) y validación para evitar leakage.
- Entrenamiento y selección por métricas de ranking (AUC/KS) y/o calibración (Brier / reliability).
- Exposición por API y monitoreo: drift de variables + performance por ventanas.

## Results
- Metric(s): <completa>
- Key insight: En riesgo, además de AUC/KS, la calibración y el monitoreo son críticos para decisiones consistentes.

## Demo
- API: <link o "local">
- Dashboard/Monitoring: <link o "local">

## How to run
- Install:
  - `pip install -r requirements.txt`
- Run (si aplica):
  - `uvicorn app.main:app --reload`
  - `streamlit run app/app.py`

## Repo structure
- `src/` lógica de datos/features/modelo
- `app/` API y/o dashboard
- `tests/` pruebas (si aplica)
- `reports/` figuras y resultados

## Next steps
- Definir política de decisión: umbral por costo + revisión manual.
- Agregar explainability (SHAP) y reportes de estabilidad (PSI/KS por feature).
