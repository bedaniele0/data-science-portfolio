# Feature Engineering Overview

**Proyecto**: Walmart Demand Forecasting & Inventory Optimization  
**Fecha**: 2026-02-06  

## Features principales

- **Calendar**: día de la semana, mes, eventos.
- **Lag**: ventas lag 1, 7, 28.
- **Rolling**: media y std en ventanas.
- **Precio**: nivel y cambios de precio.
- **Eventos/SNAP**: flags por estado y tipo de evento.

## Artefactos

- `data/processed/sales_with_features.parquet`
- `data/processed/feature_catalog.txt`
- `models/feature_importance_lgb.csv`

## Referencias

- `docs/04_feature_catalog.md`
- `src/features/`
