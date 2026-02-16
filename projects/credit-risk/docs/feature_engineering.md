# Feature Engineering Summary - Credit Risk Scoring

**Autor:** Ing. Daniel Varela Perez  
**Email:** bedaniele0@gmail.com  
**Fecha:** 2026-02-04  
**Versión:** 1.0

---

## 1. Objetivo
Transformar variables raw en features de riesgo crediticio con señales de utilización, capacidad de pago y segmentación demográfica.

## 2. Features derivadas (13)
- `utilization_1`
- `payment_ratio_1` ... `payment_ratio_6`
- `AGE_bin_26-35`, `AGE_bin_36-45`, `AGE_bin_46-60`, `AGE_bin_60+`
- `EDUCATION_grouped`
- `MARRIAGE_grouped`

## 3. Implementación
- Script: `src/features/build_features.py`
- Salida: `data/processed/featured_dataset.csv` y `data/processed/dataset_final.csv`

## 4. Catálogo
Ver `docs/07_feature_catalog.md` y `src/features/feature_catalog.csv`.

---

**© 2026 - DVP-MASTER Framework - Ing. Daniel Varela Perez**
