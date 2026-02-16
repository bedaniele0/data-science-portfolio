# Lessons Learned - Prediccion de User Score

Autor: Ing. Daniel Varela Perez
Email: bedaniele0@gmail.com
Tel: +52 55 4189 3428
Fecha: 2026-02-06
Version: 1.1

---

## 1. Lo que funciono
- Multi-hot controlado en `genres` (Top 20) y pipeline reproducible.
- Evaluacion comparativa con varios modelos.

## 2. Lo que no funciono
- R2 no llego a 0.50 pese a mejorar el encoding de `genres`.

## 3. Riesgos materializados
- Missing en `user_score` y `meta_score` afecta capacidad explicativa.

## 4. Recomendaciones para futuros proyectos
- Expandir vocabulario de genres y probar XGBoost/LightGBM.
- Evaluar split temporal como mejora futura.
