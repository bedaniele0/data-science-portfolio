# Handoff to Optimization (F9 -> MO)

**Proyecto:** Credit Risk Scoring (UCI Taiwan)  
**Fecha:** 2026-02-04  
**Estado:** AMARILLO (SIMULADO)

---

## 1. Estado actual
- F9 completado en modo SIMULADO.
- Estado AMARILLO por falta de KPIs reales y ROI observado >= 3 meses.

## 2. Métricas afectadas
- AUC: 0.7813 (objetivo 0.80 no alcanzado)
- Fairness audit: pendiente
- KPIs de negocio: no medidos en producción

## 3. Evidencia objetiva
- `docs/11_final_report.md`
- `docs/roi_validation.md`
- `docs/lessons_learned.md`
- `reports/metrics/validation_results.json`

## 4. Recomendaciones previas
- Ejecutar piloto real con medición >= 3 meses
- Completar fairness audit (SEX, AGE)
- Mejorar AUC con features adicionales/ensembles

## 5. Ventana analizada
- SIMULADA (no producción real)
- Referencia: 2025-10-01 a 2025-12-31
- Current: 2026-01-01 a 2026-01-31

---

