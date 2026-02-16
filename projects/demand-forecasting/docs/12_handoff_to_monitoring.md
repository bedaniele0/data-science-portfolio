# Handoff to Monitoring (F7)

**Proyecto**: Walmart Demand Forecasting & Inventory Optimization  
**Fecha**: 2026-02-06  

## Resumen

El proyecto está listo para monitoreo en modo demo/portafolio.  
Modelo LightGBM entrenado con features engineered del dataset M5.

## Artefactos clave

- Modelo: `models/lightgbm_model.pkl`
- Features: `data/processed/sales_with_features.parquet`
- API: `src/api/`
- Dashboard: `src/visualization/` (si aplica)

## Señales a monitorear

- Métricas de error (MAE/WRMSSE)
- Drift en features y demanda
- Latencia de predicción
