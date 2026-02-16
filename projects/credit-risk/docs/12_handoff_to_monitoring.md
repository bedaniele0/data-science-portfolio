# Handoff to Monitoring (F7 -> F8)

**Proyecto:** Credit Risk Scoring (UCI Taiwan)  
**Fecha:** 2026-02-04  
**Responsable:** Ing. Daniel Varela Perez

---

## 1. Resumen del Modelo
- Modelo final: CalibratedClassifierCV (LightGBM + isotonic)
- Threshold operativo: 0.12
- Features: 36 (`models/feature_names.json`)

## 2. Artefactos Entregados
- `models/final_model.joblib`
- `models/model_metadata.json`
- `models/feature_names.json`
- `reports/metrics/validation_results.json`
- `reports/backtest_or_validation.json`

## 3. Métricas Base
- AUC: 0.7813
- KS: 0.4251
- Recall (thr=0.12): 0.8704
- Precision (thr=0.12): 0.3107
- Brier: 0.1349

## 4. Monitoreo Requerido
- Drift PSI/KS mensual
- Alertas si PSI > 0.25 o KS decay > 10%

## 5. Owner
MLOps / Data Science

---

