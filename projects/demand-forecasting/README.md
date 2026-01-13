# Walmart Demand Forecasting (E2E)

**One-liner:** Plataforma end-to-end para pronosticar demanda (M5/Walmart) y habilitar planeación de inventario vía API y dashboard.  
**Stack:** Python, pandas, LightGBM/ML, MLflow (si aplica), FastAPI, Streamlit.  
**Deliverable:** Pipeline reproducible + tracking (si aplica) + API + Dashboard.  
**Results:** <completa: RMSE/WRMSSE/MAPE u otra métrica del proyecto>.

## Problem
Predecir la demanda futura por tienda/producto para soportar decisiones de inventario y reposición, minimizando errores y evitando leakage temporal.

## Data
- Source: M5 Forecasting (Walmart) / Kaggle (si aplica)
- Size: <completa: #series / periodo / filas>

## Approach
- Feature engineering temporal (lags, rolling stats, calendarios/eventos, precios).
- Backtesting con split temporal y evaluación consistente.
- Modelo (LightGBM u otro) + registro/experimentos (si aplica) y exposición mediante API/dashboard.

## Results
- Metric(s): <completa>
- Key insight: Las variables de calendario/eventos + lags/rolling capturan estacionalidad y mejoran el desempeño vs baselines.

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
- Agregar intervalos de predicción (quantiles) para decisiones de stock.
- Monitoreo de drift estacional y performance por familia/categoría.
