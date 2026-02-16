# Final Report - Prediccion de User Score

Autor: Ing. Daniel Varela Perez
Email: bedaniele0@gmail.com
Tel: +52 55 4189 3428
Fecha: 2026-02-06
Version: 2.0

---

## 1. Executive Summary
- Problema: Estimar `user_score` y entender drivers de percepcion del usuario.
- Resultado: RandomForest con MAE 0.577 y R2 0.451.
- Impacto: Proyecto de portafolio con pipeline reproducible y analisis de features.
- Estado: AMARILLO (SIMULADO) por ausencia de KPIs reales.

## 2. Resultados vs Objetivos
| Metrica | Objetivo (F0) | Alcanzado | Status |
|---|---|---|---|
| MAE | ≤ 0.60 | 0.577 | OK |
| R2 | ≥ 0.50 | 0.451 | NO |
| KPI negocio | Insights accionables | Identificados drivers clave | OK |

## 3. Impacto Estimado
- Beneficio: Caso de portafolio con analisis y modelado reproducibles.
- Costo del proyecto: 3-4 dias de trabajo individual.
- ROI estimado: Cualitativo alto (portafolio).

## 4. Limitaciones
- Missing relevante en `user_score` (24%) y `meta_score` (36%).
- R2 permanece debajo del objetivo tras multi-hot de genres.

## 5. Recomendacion
- Decision: Mantener en AMARILLO (SIMULADO) hasta contar con KPIs reales.
- Proximo paso: ampliar vocabulario de genres y evaluar modelos boosting adicionales en retraining.

## 6. Arquitectura Final (SIMULADA)
- Cloud: AWS (diseño)
- Orquestacion: EventBridge Scheduler + ECS Fargate (diseño)
- Storage: S3 (input/predictions/actuals/monitoring) (diseño)
- Schedule: Batch diario 02:00 UTC (diseño)
- Owners: DS/ML Engineer (tecnico), Product/Analytics Lead (negocio)
- Umbrales activos: PSI 0.20/0.30, MAE +10%/+20%, R2 -0.05/-0.10
- Retraining: mensual o por drift critico

---

**© 2026 - DVP-MASTER Framework - Ing. Daniel Varela Perez**
