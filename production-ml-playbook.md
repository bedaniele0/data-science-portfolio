# Production ML Playbook (mini)

Este documento resume el “sistema operativo” que uso para llevar modelos a producción y operarlos de forma confiable.
Los proyectos del portafolio sirven como evidencia (API/batch, monitoreo, runbooks).

## 1) Data validation (antes de entrenar y antes de inferir)
- Contrato mínimo: schema (tipos), rangos, nulos permitidos, categorías válidas.
- Suites de validación (ej. Great Expectations o validadores propios) y reportes reproducibles.
- Política de fallo: **fail-fast** si rompe contrato crítico; degradación controlada si es no-crítico.

## 2) Training & evaluation (reproducible)
- Seeds fijos, splits documentados (temporal si aplica), baseline + candidato.
- Artefactos versionados: dataset snapshot, features, modelo, métricas, config.
- Registro de experimentos (ej. MLflow) y criterios de promoción.

## 3) Release packaging & traceability
- Paquete de release con:
  - `model.pkl`/`model.joblib`
  - `config.yaml`
  - `metrics.json`
  - `manifest.json` (versiones, paths, checksums)
- Verificación de integridad por hash antes de desplegar.
- Plan de rollback (artefacto anterior + runbook).

## 4) Deployment (API o batch)
- API: validación de entrada (Pydantic), timeouts, límites, logging estructurado.
- Batch: idempotencia, rutas claras de input/output, reintentos controlados.

## 5) Monitoring & drift
- Drift de datos: PSI/KS por feature, ventanas (diaria/semanal).
- Performance: métricas con labels (cuando existan), alertas por umbral.
- Operación: latencia p95, errores, throughput (si aplica).

## 6) Shadow testing (promoción segura)
Checklist:
- Modelo candidato corre en sombra con el mismo tráfico/dataset.
- Comparación de métricas + latencia.
- Criterios de promoción y “kill switch”.

## 7) Runbooks & handoffs
- Runbook por pipeline: cómo ejecutar, cómo validar, cómo investigar drift, cómo rollback.
- Post-analysis: qué métricas revisar, cómo abrir issue y priorizar mejoras.
