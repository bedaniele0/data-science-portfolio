# Monitoring Runbook (F8)

**Proyecto**: Walmart Demand Forecasting & Inventory Optimization  
**Fecha**: 2026-02-06  

## Objetivo

Definir cómo monitorear drift y performance del modelo en modo demo/portafolio.

## Señales

- PSI por feature
- KS por demanda
- Latencia de predicción (p95)

## Frecuencia

- Mensual (simulado)

## Respuesta a incidentes

- PSI > 0.2 → investigar drift y reentrenar
- Latencia p95 > 200 ms → revisar feature store y caché
