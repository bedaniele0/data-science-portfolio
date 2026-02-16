# Monitoring Report - Credit Risk Scoring

**Proyecto:** Credit Risk Scoring (UCI Taiwan)  
**Fecha:** 2026-02-04  
**Estado:** VERDE (SIMULADO)  
**Canal:** API FastAPI en Docker

---

## 1. Ventanas de Monitoreo
- **REFERENCE:** 2025-10-01 a 2025-12-31  
- **CURRENT:** 2026-01-01 a 2026-01-31  
- **Modo:** SIMULADO (no producción real)

## 2. Métricas Base (del Handoff)
- AUC: 0.7813
- KS: 0.4251
- Recall (thr=0.12): 0.8704
- Precision (thr=0.12): 0.3107
- Brier: 0.1349

## 3. Monitoreo de Drift (SIMULADO)
**Umbrales:**
- PSI < 0.10 OK
- 0.10–0.25 WARNING
- >= 0.25 CRITICAL
- KS decay < 10% OK

**Resultado SIMULADO (re-evaluación post-MO):**
- PSI global: 0.0028 (OK)
- KS decay: N/A (sin labels en producción; simulación sin labels)
- Conclusión: sin drift relevante en CURRENT

**Evidencia:** `reports/monitoring/drift_report_20260204_154506.json`

## 4. Estado General
**VERDE (SIMULADO)**  
