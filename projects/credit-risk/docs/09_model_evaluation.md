# Model Evaluation - Credit Risk Scoring

**Autor:** Ing. Daniel Varela Perez  
**Email:** bedaniele0@gmail.com  
**Fecha:** 2026-02-04  
**Versión:** 1.0

---

## 1. Resumen
Evaluación del modelo final CalibratedClassifierCV (LightGBM + isotonic) sobre el conjunto test.

## 2. Métricas principales (test)
- AUC-ROC: 0.7813
- KS: 0.4251
- Recall (thr=0.12): 0.8704
- Precision (thr=0.12): 0.3107
- Brier Score: 0.1349

## 3. Threshold óptimo
- Threshold: 0.12
- Cost savings: 5,466,000 MXN

## 4. Evidencia
- `reports/metrics/validation_results.json`
- `reports/metrics/model_comparison.csv`
- `models/final_metrics.json`

---

**© 2026 - DVP-MASTER Framework - Ing. Daniel Varela Perez**
