# Telco Churn (IBM) + ROI Policy (E2E)

**One-liner:** Predicción de churn en telecom con política de intervención basada en ROI para priorizar acciones de retención.  
**Stack:** Python, pandas, scikit-learn/LightGBM, (FastAPI/Streamlit si aplica).  
**Deliverable:** Modelo + evaluación + política de decisión (ROI) + (API/Dashboard si aplica).  
**Results:** ROI ~4.56x (según evaluación del proyecto).

## Problem
Predecir churn y decidir a quién intervenir considerando costos de retención e impacto esperado. En churn, el modelo es solo una parte: la política de acción es lo que genera valor.

## Data
- Source: IBM Telco Customer Churn (si aplica)
- Size: <completa: filas/columnas>

## Approach
- Preparación de datos (encoding, missing) y evaluación con métricas de clasificación.
- Optimización de umbral / política de intervención basada en ROI (beneficio esperado vs costo).
- (Opcional) Exposición mediante API y/o dashboard para scoring y análisis.

## Results
- Metric(s): <AUC/F1/Recall si aplica> + ROI ~4.56x
- Key insight: Un enfoque ROI convierte probabilidades en decisiones, maximizando impacto y evitando gastar en clientes con bajo retorno.

## Demo
- API: <link o "local">
- Dashboard: <link o "local">

## How to run
- Install:
  - `pip install -r requirements.txt`
- Run (si aplica):
  - `uvicorn app.main:app --reload`
  - `streamlit run app/app.py`

## Repo structure
- `src/` lógica de datos/features/modelo
- `app/` API y/o dashboard
- `reports/` figuras y resultados
- `tests/` pruebas (si aplica)

## Next steps
- Calibración de probabilidades y análisis por segmento (tenure, plan, region).
- Monitoreo de performance y drift por ventana temporal.
