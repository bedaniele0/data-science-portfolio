# KPI Tree - Prediccion de User Score

Autor: Ing. Daniel Varela Perez
Email: bedaniele0@gmail.com
Tel: +52 55 4189 3428
Fecha: 2026-02-06
Version: 1.0

---

## 1. Objetivo de Negocio (North Star)
- Objetivo: Anticipar la percepcion del usuario y detectar drivers del `user_score`
- Horizonte: corto plazo (proyecto 3-4 dias)

## 2. KPIs Principales
| KPI | Definicion | Formula | Baseline | Objetivo | Owner |
|---|---|---|---|---|---|
| Calidad del modelo | Desempeno del modelo de regresion | MAE y R2 en validacion | N/A | MAE ≤ 0.60, R2 ≥ 0.50 | DS |
| Insights accionables | Variables con influencia clara | Top features con interpretacion | N/A | Top 5 drivers | DS |

## 3. KPIs Leading vs Lagging
| Tipo | KPI | Frecuencia | Fuente de Datos | Notas |
|---|---|---|---|---|
| Leading | MAE en validacion | Una vez | data.csv | Modelo baseline
| Lagging | Insights documentados | Una vez | Reporte EDA | Relevancia cualitativa

## 4. Arbol de Metricas (Jerarquia)
- North Star: Percepcion de usuario anticipada
  - Driver 1: Calidad del modelo (MAE/R2)
    - Sub-metrica: RMSE
  - Driver 2: Interpretabilidad
    - Sub-metrica: importancia de variables

## 5. Supuestos y Riesgos
- Supuesto 1: `meta_score` y variables categoricas tienen señal explicativa.
- Riesgo 1: `user_score` con muchos valores faltantes.

## 6. Validacion
- Aprobado por: Ing. Daniel Varela Perez
- Fecha: 2026-02-06
