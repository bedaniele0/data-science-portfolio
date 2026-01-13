# Customer Churn Prediction (E2E)

**One-liner:** Sistema end-to-end para predecir churn y priorizar acciones de retención con enfoque costo/beneficio (umbral operativo).  
**Stack:** Python, pandas, scikit-learn/LightGBM, FastAPI, Streamlit (si aplica).  
**Deliverable:** Pipeline reproducible + API + (dashboard) + recomendación de umbral.  
**Results:** Recall ~92.5% (según evaluación del proyecto) + política de decisión (si aplica).

## Problem
Predecir qué clientes tienen mayor probabilidad de abandonar para enfocar campañas de retención. La parte crítica es decidir el **umbral** según costos: retener a quien no se iba (FP) vs perder a quien sí se iba (FN).

## Data
- Source: <completa: público / Kaggle / IBM Telco / otro>
- Size: <completa: filas/columnas>

## Approach
- EDA + preparación (missing, encoding, escalado si aplica).
- Entrenamiento de modelo y evaluación con métricas de clasificación (AUC, precision/recall, F1).
- Optimización de umbral con criterio de negocio (costo-beneficio / ROI si aplica).
- Exposición mediante API y dashboard para scoring y exploración.

## Results
- Metric(s): Recall ~92.5% (y/o AUC/F1 si aplica)
- Key insight: Ajustar umbral por costo suele mejorar valor de negocio frente a maximizar una sola métrica.

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
- Calibración de probabilidades y análisis por segmentos (plan, región, tenure).
- Monitoreo: performance y drift por ventana temporal.
