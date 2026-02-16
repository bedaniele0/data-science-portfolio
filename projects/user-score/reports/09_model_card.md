# Model Card - Prediccion de User Score

Autor: Ing. Daniel Varela Perez
Email: bedaniele0@gmail.com
Tel: +52 55 4189 3428
Fecha: 2026-02-06
Version: 1.0

---

## 1. Resumen del Modelo
- Tipo: regresion
- Algoritmo: RandomForestRegressor
- Version: v1.0

## 2. Datos
- Fuente: data.csv (training) + batch diario (SIMULADO)
- Periodo: 1996-09-26 a 2021-02-12
- Target: user_score

## 3. Metricas (holdout test)
- MAE: 0.577
- RMSE: 0.808
- R2: 0.451

## 4. Uso Previsto
- Estimar percepcion del usuario para priorizar mejoras de producto/contenido.
- Soporte a analisis de factores que influyen en user_score.

## 5. Limitaciones
- Missing relevante en user_score y meta_score.
- Alta cardinalidad en genres y developers.
- R2 por debajo del objetivo 0.50.

## 6. Consideraciones Eticas
- No hay datos sensibles personales.
- Riesgo de interpretacion excesiva: usar como apoyo, no como verdad absoluta.

---

**© 2026 - DVP-MASTER Framework - Ing. Daniel Varela Perez**
