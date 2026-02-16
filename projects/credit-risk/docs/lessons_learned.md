# Lessons Learned (F9)

**Proyecto:** Credit Risk Scoring (UCI Taiwan)  
**Fecha:** 2026-02-04

---

## 1. Qué funcionó bien
- Pipeline de features alineado con API y modelos.
- Métricas técnicas cumplen 4/5 objetivos.
- Documentación completa F0–F8.

## 2. Qué mejorar
- AUC ligeramente bajo (0.7813 vs 0.80).
- Falta fairness audit real.
- Validar ROI con datos de producción >= 3 meses.

## 2.1 Re‑evaluación post‑MO
- Monitoreo actualizado sin drift (SIMULADO).
- No hay cambios en KPIs de negocio por falta de datos reales.

## 3. Próximos pasos recomendados
- Ejecutar piloto real y medir KPIs negocio.
- Monitoreo continuo y retraining si PSI > 0.25.
- Completar auditoría de fairness.
