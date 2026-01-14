# Telco Churn (IBM) + ROI Policy (E2E)

**One-liner:** Predicción de churn en telecom con política de intervención basada en ROI para priorizar acciones de retención.  
**Stack:** Python, pandas, scikit-learn/LightGBM, FastAPI, Streamlit.  
**Deliverable:** Modelo + evaluación + política ROI + API/Dashboard.  
**Results:** AUC 0.832, F1 0.624, Recall 0.807, Precision 0.508, ROI 4.56x.

## Problem
Predecir churn y decidir a quién intervenir considerando costos de retención e impacto esperado. En churn, el modelo es solo una parte: la política de acción es lo que genera valor.

## Data
- Source: IBM Telco Customer Churn
- Size: 7,043 filas x 21 columnas (raw)

## Approach
- Preparación de datos (encoding, missing) y evaluación con métricas de clasificación.
- Optimización de umbral / política de intervención basada en ROI (beneficio esperado vs costo).
- (Opcional) Exposición mediante API y/o dashboard para scoring y análisis.

## Results
- Metric(s): AUC 0.832, F1 0.624, Recall 0.807, Precision 0.508 + ROI 4.56x
- Key insight: Un enfoque ROI convierte probabilidades en decisiones, maximizando impacto y evitando gastar en clientes con bajo retorno.

## Impact
- Objetivo de negocio: reducir riesgo o mejorar decision operativa
- Solucion: pipeline end-to-end con modelo + API + dashboard
- Metrica clave: ver seccion Results
- ROI demo: ver seccion Results si aplica

## Dashboard
<img src="../../assets/images/telco-dashboard-2.png" style="width:100%; max-width:100%; height:auto;" alt="Telco churn dashboard">
<em>Vista del dashboard</em><br>

## Demo
- API: local (`uvicorn src.api.main:app --reload`)
- Dashboard: local (`streamlit run dashboard/app.py`)

## How to run
- Install:
  - `pip install -r requirements.txt`
- Run:
  - `uvicorn src.api.main:app --reload`
  - `streamlit run dashboard/app.py`

## Repo structure
- `src/` pipelines y API
- `dashboard/` Streamlit
- `docs/` entregables por fase

## Next steps
- Calibración de probabilidades y análisis por segmento (tenure, plan, region).
- Monitoreo de performance y drift por ventana temporal.
