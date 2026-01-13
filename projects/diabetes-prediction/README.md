# Clinical Diabetes Prediction Platform (E2E)

**One-liner:** Plataforma end-to-end para predicción de diabetes con explicabilidad (SHAP) y consumo vía API + dashboard (si aplica).  
**Stack:** Python, pandas, scikit-learn/LightGBM, SHAP, FastAPI, Streamlit (si aplica).  
**Deliverable:** Pipeline reproducible + API + (dashboard) + explicabilidad.  
**Results:** <completa: AUC/F1/Recall u otra métrica del proyecto>.

## Problem
Apoyar detección temprana estimando riesgo de diabetes a partir de variables clínicas. Importante: interpretar predicciones (explicabilidad) para confianza y adopción.

## Data
- Source: <completa: público / Kaggle / otro>
- Size: <completa: filas/columnas>

## Approach
- Preparación de datos (missing, escalado/encoding si aplica).
- Entrenamiento y evaluación con validación adecuada; selección por métricas (AUC/F1/Recall).
- Explicabilidad con **SHAP** para entender drivers del riesgo.
- Exposición vía API (y dashboard si aplica) para uso interactivo.

## Results
- Metric(s): <completa>
- Key insight: SHAP permite explicar qué variables empujan el riesgo por paciente, facilitando revisión y confianza del modelo.

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
- Calibración y análisis de umbrales (sensibilidad vs especificidad).
- Evaluación de fairness (si hay variables sensibles) y validación temporal/geográfica si aplica.
