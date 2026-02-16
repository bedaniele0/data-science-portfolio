# Data Quality Report (F3)

**Proyecto**: Walmart Demand Forecasting & Inventory Optimization  
**Fecha**: 2026-02-06  

## Resumen

Evaluación de calidad de datos del dataset M5 (Walmart) usado en la demo. El reporte se basa en los archivos `data/raw/` y validaciones del pipeline local.

## Checks principales

- **Completitud**: sin nulos en llaves (`item_id`, `store_id`, `d_*`, `wm_yr_wk`).
- **Consistencia temporal**: calendario con 1,969 días (2011-01-29 a 2016-06-19).
- **Duplicados**: no se detectaron duplicados en llaves de `sell_prices` (`store_id`, `item_id`, `wm_yr_wk`).
- **Valores extremos**: ventas diarias con alta dispersión y fuerte cero‑inflación (esperado en retail).
- **Precios**: `sell_price` > 0 en registros disponibles.

## Hallazgos

- **Zero‑inflation** alta (~68%) en series de ventas.
- **Datos históricos** (hasta 2016), útiles para demo/portafolio pero no actuales.
- **Variabilidad de precios** significativa, requiere features de precio y promo.

## Riesgos y mitigación

- **Riesgo**: modelos sensibles a ceros en demanda.  
  **Mitigación**: features de lags/rolling + modelos robustos (LightGBM).

- **Riesgo**: drift temporal fuera de rango histórico.  
  **Mitigación**: monitoreo y retraining periódico.

## Evidencia

- `docs/03_eda_report.md`
- `notebooks/01_eda_executed.ipynb`
