# Model Evaluation Report - Prediccion de User Score

**Autor**: Ing. Daniel Varela Perez
**Email**: bedaniele0@gmail.com
**Tel**: +52 55 4189 3428
**Fecha**: 19/01/2026
**Modelo**: RandomForest

---

## 1. Nota sobre tipo de problema
Este es un problema de **regresion**. No aplica matriz de confusion ni metricas de clasificacion.

---

## 2. Performance Metrics

### Resultados por modelo (test)
| Modelo | MAE | RMSE | R2 |
|---|---|---|---|
| GradientBoosting | 0.568 | 0.811 | 0.447 |
| LinearRegression | 0.568 | 0.809 | 0.451 |
| RandomForest | 0.577 | 0.808 | 0.451 |


### Comparacion vs objetivos
| Metrica | Valor | Objetivo | Status |
|---|---|---|---|
| MAE | 0.577 | ≤ 0.60 | ✅ |
| R2 | 0.451 | ≥ 0.50 | ❌ |

---

## 3. Feature Importance (Top 10, GradientBoosting)
| Feature | Importance |
|---|---|
| num__meta_score | 0.5164 |
| num__date_year | 0.1977 |
| num__date_month | 0.0456 |
| cat__platform_iOS | 0.0408 |
| genre__genre_Miscellaneous | 0.0344 |
| genre__genre_Edutainment | 0.0290 |
| cat__esrb_rating_E | 0.0202 |
| genre__genre_Console-style RPG | 0.0183 |
| genre__genre_Action | 0.0128 |
| cat__platform_DS | 0.0123 |


---

## 4. Decision de modelo
- **Modelo recomendado**: RandomForest (mejor R2 actual)
- **Riesgo**: R2 no alcanza el objetivo de 0.50.

---

## 5. Observaciones
- Se implemento multi-hot controlado para `genres` (Top 20).
- MAE se mantiene en el umbral, pero R2 sigue por debajo del objetivo.
- Posible mejora: aumentar vocabulario de genres y probar XGBoost/LightGBM.

---

**© 2026 - DVP-MASTER Framework - Ing. Daniel Varela Perez**
