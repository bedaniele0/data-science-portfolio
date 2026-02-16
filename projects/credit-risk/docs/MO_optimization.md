# MO - Plan de Optimización (Credit Risk Scoring)

**Proyecto:** Credit Risk Scoring (UCI Taiwan)  
**Fecha:** 2026-02-04  
**Estado base:** AMARILLO (SIMULADO)

---

## 1. Diagnóstico y Métricas Afectadas
- **AUC**: 0.7813 (< 0.80 objetivo)
- **Fairness**: pendiente (SEX, AGE, EDUCATION)
- **KPIs de negocio**: no medidos en producción real

## 2. Hipótesis de Mejora
1. Features externas (ingresos, bureau score) mejorarán AUC.
2. Ensemble (LightGBM + XGBoost) elevará AUC y estabilidad.
3. Ajustes de calibración (sigmoid vs isotonic) podrían mejorar AUC sin degradar Brier.
4. Threshold dinámico por segmento puede mejorar KPI negocio.

## 3. Experimentos Propuestos
- **E1:** Agregar features externas simuladas (proxy) y medir AUC.
- **E2:** Ensemble (stacking) con LightGBM + XGBoost + LogReg.
- **E3:** Comparar calibración isotonic vs sigmoid (Brier + AUC).
- **E4:** Threshold optimization por segmento (edad/educación).

## 4. Plan de Ejecución y Evidencia
- Actualizar pipeline de features (`src/features/build_features.py`).
- Entrenar con nuevos datasets y comparar métricas (`reports/metrics/model_comparison.csv`).
- Ejecutar fairness audit y documentar resultados.
- Registrar en MLflow y documentar en `reports/`.

## 5. Criterios de Éxito y Handoff
- **AUC ≥ 0.80**
- **Fairness audit aprobado**
- **KPIs negocio medidos** (>= 3 meses) y ROI >= media
- Handoff a monitoreo: `docs/15_handoff_to_monitoring.md`

---

