# Fraud Detection System (E2E)

**One-liner:** Sistema end-to-end para detectar transacciones fraudulentas y habilitar decisiones operativas vía API y dashboard.  
**Stack:** Python, pandas, scikit-learn/LightGBM, FastAPI, Streamlit, JWT, Docker (si aplica).  
**Deliverable:** API (FastAPI) + Dashboard (Streamlit) + pipeline reproducible.  
**Results:** ROC-AUC 95.28%, Precision 93.62%, Recall 72.13% (test set).

## Problem
Detectar fraude en transacciones con foco en minimizar falsos negativos sin disparar falsos positivos, habilitando consumo del modelo por sistemas internos mediante una API segura.

## Data
- Source: Kaggle Credit Card Fraud Detection (dataset público)
- Size: 284,807 transacciones, 30 features + Time/Amount + target

## Approach
- Limpieza y preparación de datos + validación para evitar leakage.
- Entrenamiento y comparación de modelos; selección por métricas (ROC-AUC, PR-AUC / F1 según caso).
- Exposición del modelo mediante FastAPI con autenticación JWT y visualización de resultados en dashboard.

## Results
- Metric(s): ROC-AUC 95.28%, Precision 93.62%, Recall 72.13%, F1 81.48%
- Key insight: Ajustar umbral según costo de FN/FP mejora la utilidad operativa frente a optimizar solo una métrica global.
  - ROI demo (supuestos conservadores): ahorro potencial ~$25.9M/año, conservador ~$7.8M/año

## Demo
- API: local (`fraud-api` o `uvicorn api.main:app --reload`)
- Dashboard: local (`fraud-dashboard`)

## How to run
- Install:
  - `pip install -r requirements.txt`
- Run:
  - `fraud-api`
  - `fraud-dashboard`

## Repo structure
- `src/` lógica de datos/features/modelo
- `app/` API y/o dashboard
- `tests/` pruebas (si aplica)
- `reports/` figuras y resultados

## Next steps
- Agregar calibración (Platt/Isotonic) si el output se usa como probabilidad.
- Monitoreo de drift + performance (PSI, métricas por ventana temporal).
