# F4 - Feature Engineering

**Proyecto**: Walmart Demand Forecasting & Inventory Optimization  
**Fecha**: 2026-02-06  

## Resumen

Se implementó un pipeline de feature engineering para forecasting diario por producto‑tienda (M5), incorporando lags, rolling stats, calendario, precios y eventos SNAP.

## Pipeline

- **Código**: `src/features/`
- **Notebook ejecutado**: `notebooks/02_feature_engineering_executed.ipynb`

## Salidas

- `data/processed/sales_with_features.parquet`
- `data/processed/dataset.parquet`
- `data/processed/feature_catalog.txt`

## Evidencia

- `docs/04_feature_catalog.md`
