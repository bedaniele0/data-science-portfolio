# Fraud Detection System (E2E)

**One-liner:** Sistema end-to-end para detectar transacciones fraudulentas y habilitar decisiones operativas vía API y dashboard.  
**Stack:** Python, pandas, scikit-learn/LightGBM, FastAPI, Streamlit, JWT, Docker (si aplica).  
**Deliverable:** API (FastAPI) + Dashboard (Streamlit) + pipeline reproducible.  
**Results:** ROC-AUC ~95.9% (según evaluación del proyecto).

## Problem
Detectar fraude en transacciones con foco en minimizar falsos negativos sin disparar falsos positivos, habilitando consumo del modelo por sistemas internos mediante una API segura.

## Data
- Source: <completa: Kaggle / público / otro>
- Size: <completa: filas/columnas>

## Approach
- Limpieza y preparación de datos + validación para evitar leakage.
- Entrenamiento y comparación de modelos; selección por métricas (ROC-AUC, PR-AUC / F1 según caso).
- Exposición del modelo mediante FastAPI con autenticación JWT y visualización de resultados en dashboard.

## Results
- Metric(s): ROC-AUC ~95.9%
- Key insight: Ajustar umbral según costo de FN/FP mejora la utilidad operativa frente a optimizar solo una métrica global.

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
- `tests/` pruebas (si aplica)
- `reports/` figuras y resultados

## Next steps
- Agregar calibración (Platt/Isotonic) si el output se usa como probabilidad.
- Monitoreo de drift + performance (PSI, métricas por ventana temporal).
