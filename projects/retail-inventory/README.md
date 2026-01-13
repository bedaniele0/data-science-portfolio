# Retail Inventory Demand + Restocking Plan (E2E)

**One-liner:** Sistema end-to-end para predecir demanda y generar un plan de reabastecimiento, con entrega vía API y dashboard (si aplica).  
**Stack:** Python, pandas, modelo de forecasting/clasificación (según tu enfoque), FastAPI, Streamlit (si aplica).  
**Deliverable:** Pipeline reproducible + API + (dashboard) + recomendación de restock.  
**Results:** <completa: métrica de forecast y/o KPI operativo (fill rate, stockouts evitados, etc.)>.

## Problem
Predecir demanda y transformar predicciones en decisiones accionables de inventario: cuánto reabastecer y cuándo, para reducir quiebres de stock y exceso de inventario.

## Data
- Source: <completa: público / Kaggle / otro>
- Size: <completa: SKUs, tiendas, periodo>

## Approach
- Preparación de datos + features (temporales, promociones, estacionalidad si aplica).
- Pronóstico / predicción de demanda y evaluación con split temporal.
- Lógica de reabastecimiento (reglas + parámetros: lead time, safety stock, reorder point).
- Exposición mediante API y visualización en dashboard para planeación.

## Results
- Metric(s): <completa>
- Key insight: Convertir forecast en política de restocking (ROP/safety stock) conecta ML con impacto operativo.

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
- Simulación de inventario para comparar políticas (baseline vs ML-driven).
- Métricas de negocio: stockouts, overstock, fill rate, costo total.
