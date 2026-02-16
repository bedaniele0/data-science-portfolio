# Data Sources (F2)

**Proyecto**: Walmart Demand Forecasting & Inventory Optimization  
**Fecha**: 2026-02-06  

## Fuente principal

- **M5 Forecasting (Walmart)**, competencia Kaggle.
- Descarga y acceso detallados en `docs/DATA_ACCESS.md`.

## Archivos RAW (ingesta)

- `data/raw/sales_train_validation.csv`
- `data/raw/sales_train_evaluation.csv`
- `data/raw/calendar.csv`
- `data/raw/sell_prices.csv`
- `data/raw/sample_submission.csv`

## Archivos procesados (pipeline)

- `data/processed/train_data.csv`
- `data/processed/valid_data.csv`
- `data/processed/test_data.parquet`
- `data/processed/sales_with_features.parquet`
- `data/processed/dataset.parquet`

## Notas

- Datos historicos 2011-2016 (no actuales).
- Uso enfocado a demo/portafolio y reproducibilidad local.
