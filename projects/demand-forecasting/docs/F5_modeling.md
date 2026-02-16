# F5 - Modeling Summary

**Proyecto**: Walmart Demand Forecasting & Inventory Optimization  
**Fecha**: 2026-02-06  

## Resumen

Se entrenaron modelos baseline y avanzados para forecasting. El modelo seleccionado es LightGBM con features engineered (lags, calendar, price, events).

## Evidencia

- Notebook baseline: `notebooks/03_baseline_modeling_executed.ipynb`
- Notebook advanced: `notebooks/04_advanced_modeling_executed.ipynb`
- Métricas training: `reports/metrics/training_metrics.json`
- Métricas latest: `reports/model_metrics_latest.json`
- Modelo final: `models/lightgbm_model.pkl` / `models/best_model.pkl`

## Código

- Entrenamiento: `src/models/train_demand.py`
- Wrapper estándar: `src/models/train.py`
