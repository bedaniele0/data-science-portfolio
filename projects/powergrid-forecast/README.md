# PowerGrid Analytics — Energy Demand Forecasting (E2E)

**One-liner:** Sistema end-to-end para pronóstico de demanda energética y soporte a operación (API + monitoreo + buenas prácticas).  
**Stack:** Python, pandas, modelo de forecasting (LightGBM/ML u otro), FastAPI, (Streamlit si aplica), tests/monitoring (si aplica).  
**Deliverable:** Pipeline reproducible + API + (dashboard/monitoring si aplica).  
**Results:** MAPE ~5.10% (según evaluación del proyecto).

## Problem
Pronosticar demanda eléctrica para apoyar planeación operativa y reducir riesgo de sobre/sub-contratación. El reto central es manejar estacionalidad, patrones horarios y evitar leakage temporal.

## Data
- Source: <completa: público / Kaggle / otro>
- Size: <completa: periodo, granularidad (hora/día), filas>

## Approach
- Preparación de serie(s): limpieza, manejo de faltantes y creación de variables temporales.
- Backtesting con split temporal (walk-forward o ventanas) para evaluación realista.
- Servicio del modelo mediante API; y si aplica, monitoreo de drift/performance por ventana.

## Results
- Metric(s): MAPE ~5.10%
- Key insight: La evaluación temporal (backtesting) es clave; un split aleatorio puede inflar métricas y no generaliza.

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
- Intervalos de predicción (P10/P50/P90) para decisiones bajo incertidumbre.
- Monitoreo de drift estacional y performance por región/segmento temporal.
