# Drift Interpretation Guide (F8)

**Proyecto**: Walmart Demand Forecasting & Inventory Optimization  
**Fecha**: 2026-02-06  

## Umbrales sugeridos

- PSI < 0.1: Sin drift relevante
- PSI 0.1–0.2: Drift moderado (monitor)
- PSI > 0.2: Drift alto (accionar)

## Acciones

- Revisar features con mayor PSI
- Validar performance del modelo
- Considerar retraining si drift persiste
