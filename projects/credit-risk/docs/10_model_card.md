# Model Card - Credit Risk Scoring Model

**Proyecto:** Credit Card Default Risk Scoring (UCI Taiwan)  
**Metodología:** DVP-PRO  
**Fase:** F7 - Deployment/Handoff  
**Autor:** Ing. Daniel Varela Pérez  
**Email:** bedaniele0@gmail.com  
**Fecha:** 2026-02-04  
**Versión:** 1.0.0

---

## 1. Model Details
- **Model Type:** Binary Classification (Credit Risk)
- **Algorithm:** LightGBM + Calibration (isotonic)
- **Framework:** scikit-learn, LightGBM
- **Model Version:** 1.0.0
- **Artifacts:** `models/final_model.joblib`, `models/final_metrics.json`, `models/model_metadata.json`

## 2. Intended Use
**Use cases**
- Predicción de probabilidad de default a 1 mes
- Bandas de riesgo: APROBADO (<20%), REVISIÓN (20-50%), RECHAZO (>=50%)

**Out of scope**
- Decisiones automáticas sin revisión humana
- Otros productos crediticios o geografías

## 3. Training Data
- **Dataset:** UCI Taiwan (2005)
- **Samples:** 30,000
- **Features:** 36 (post-ingeniería)
- **Target:** `default.payment.next.month`

## 4. Evaluation
**Métricas test (thr=0.12)**
- AUC: 0.7813
- KS: 0.4251
- Recall: 0.8704
- Precision: 0.3107
- Brier: 0.1349

**Cost savings:** 5,466,000 MXN (ver `reports/metrics/validation_results.json`)

## 5. Ethical Considerations
- Variables sensibles: SEX, AGE
- Requiere fairness audit antes de producción regulada

## 6. Limitations
- Datos de 2005, posible drift temporal
- AUC < 0.80 (ligeramente por debajo de meta)

## 7. Monitoring & Maintenance
- Drift PSI/KS mensual
- Retraining si PSI > 0.25 o KS decay > 10%

---

**© 2026 - DVP-MASTER Framework - Ing. Daniel Varela Perez**
