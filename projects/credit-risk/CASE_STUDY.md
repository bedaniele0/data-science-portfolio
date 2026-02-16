# Case Study (1 Page): Credit Risk Scoring (E2E)

## 1) Problema
Se requería estimar probabilidad de default para apoyar decisiones de crédito en un flujo operativo. El desafío era doble:
- Mantener capacidad discriminativa (separar buenos y malos pagadores).
- Entregar probabilidades útiles para decisión (no solo ranking).

En contexto crediticio, una buena métrica de ranking no basta; se necesita política de umbral y control de estabilidad para evitar degradación silenciosa.

## 2) Decisión técnica clave
La decisión principal fue diseñar el sistema para decisión de riesgo, no solo para "ganar AUC".

Se implementó:
- Pipeline de preparación y validación para evitar leakage.
- Evaluación con métricas de ranking (AUC, KS) y de probabilidad (Brier).
- Umbral operativo bajo (0.12) para priorizar recall según estrategia de riesgo.
- API de scoring y monitoreo de drift/performance para continuidad en producción.

Por qué esta decisión:
- AUC/KS indican ordenamiento, pero el negocio decide con umbral y tolerancia a riesgo.
- Calibración y monitoreo reducen decisiones inconsistentes en el tiempo.

## 3) Impacto
Resultados del proyecto:
- AUC: 0.7813
- KS: 0.4251
- Recall: 0.8704 (threshold 0.12)
- Precision: 0.3107
- Brier: 0.1349

Impacto de negocio:
- Mayor captura de casos riesgosos (recall alto) para política conservadora.
- Base técnica para gobernanza del score: API + monitoreo + trazabilidad.

Resultado para portafolio:
- Caso completo de riesgo crediticio con decisiones técnicas alineadas a negocio.
- Evidencia de criterio MLOps básico: operación, seguimiento y control de drift.
