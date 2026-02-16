# KPI Tree - Credit Risk Scoring (UCI Taiwan)

Autor: Ing. Daniel Varela Perez  
Email: bedaniele0@gmail.com  
Tel: +52 55 4189 3428  
Fecha: 04/02/2026  
Version: 1.0

---

## 1. Objetivo de Negocio (North Star)
- Objetivo: Reducir la morosidad y mejorar el margen ajustado al riesgo con un scoring predictivo.
- Horizonte: Trimestral / Anual

## 2. KPIs Principales
| KPI | Definicion | Formula | Baseline | Objetivo | Owner |
|---|---|---|---|---|---|
| Índice de morosidad | % de clientes en default | defaults / total clientes | 22.12% | 19.46% (−12% relativo) | Riesgo |
| Margen ajustado al riesgo | Margen neto / riesgo | margen neto - pérdidas esperadas | TBD | +5% | Finanzas |
| Latencia scoring | p95 tiempo de respuesta | p95(ms) | N/A | < 200 ms | MLOps |

## 3. KPIs Leading vs Lagging
| Tipo | KPI | Frecuencia | Fuente de Datos | Notas |
|---|---|---|---|---|
| Leading | AUC-ROC | semanal | métricas modelo | validación offline |
| Leading | Recall clase 1 | semanal | métricas modelo | sensibilidad de default |
| Leading | PSI drift | mensual | monitoring | alerta de drift |
| Lagging | Índice de morosidad | mensual | cartera | KPI principal |
| Lagging | Margen ajustado al riesgo | trimestral | finanzas | impacto negocio |

## 4. Arbol de Metricas (Jerarquia)
- North Star: Índice de morosidad
  - Driver 1: Precisión del scoring
    - Sub-metrica: AUC-ROC
    - Sub-metrica: KS
  - Driver 2: Calidad de decisiones
    - Sub-metrica: Recall clase 1
    - Sub-metrica: Precision clase 1
  - Driver 3: Estabilidad
    - Sub-metrica: PSI drift

## 5. Supuestos y Riesgos
- Supuesto: la distribución del dataset es representativa de la cartera actual.
- Riesgo: drift temporal puede degradar la performance.

## 6. Validacion
- Aprobado por: Ing. Daniel Varela Perez
- Fecha: 04/02/2026

---

**© 2026 - DVP-MASTER Framework - Ing. Daniel Varela Perez**
