# Monitoring Runbook - Credit Risk Scoring

**Proyecto:** Credit Risk Scoring (UCI Taiwan)  
**Fecha:** 2026-02-04  
**Canal:** API FastAPI en Docker

---

## 1. Objetivo
Operación y respuesta ante alertas de drift y degradación de performance.

## 2. Fuentes
- Reference: 2025-10-01 a 2025-12-31
- Current: 2026-01-01 a 2026-01-31 (SIMULADO)
-
## 2.1 Evidencia de monitoreo (último reporte)
- `reports/monitoring/drift_report_20260204_154506.json`

## 3. Monitoreo mínimo
- PSI global mensual
- KS decay mensual
- Latencia p95 y error rate (API)

## 4. Thresholds
- PSI < 0.10 OK
- 0.10–0.25 Warning
- >= 0.25 Critical
- KS decay < 10% OK

## 5. Acciones
- WARNING: revisar distribución de features y sample size
- CRITICAL: iniciar plan de reentrenamiento y análisis post

---
