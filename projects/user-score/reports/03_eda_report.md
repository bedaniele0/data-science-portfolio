# EDA Report - Prediccion de User Score

Autor: Ing. Daniel Varela Perez
Email: bedaniele0@gmail.com
Tel: +52 55 4189 3428
Fecha: 2026-02-06
Version: 1.0

---

## 1. Dataset Overview
- Filas: 1026
- Columnas: 9
- Target: user_score
- Periodo: 1996-09-26 a 2021-02-12

## 2. Calidad de Datos
- Missing values: meta_score (35.58%), user_score (24.27%), esrb_rating (11.31%)
- Duplicados: 0 filas duplicadas
- Outliers: metodo IQR, meta_score (9), user_score (30)

## 3. Distribucion del Target
- Rango `user_score`: 2.0 a 9.7
- Mediana: 7.9, Media: 7.70
- Grafico: `reports/figures/dist_user_score.png`

## 4. Hallazgos Clave (3-5)
1. Existe correlacion positiva moderada entre `user_score` y `meta_score` (r = 0.63).
2. `user_score` presenta valores faltantes relevantes (~24.3%), lo que exige imputacion o filtrado.
3. `meta_score` tiene missing alto (~35.6%), pero puede aportar señal cuando esta presente.
4. Variaciones de `user_score` por `esrb_rating`: categorias M y T tienden a mayor media.
5. La distribucion del target se concentra entre 7.2 y 8.4 (IQR), con pocos outliers.

## 5. Hipotesis de Negocio (3)
1. Juegos con mayor `meta_score` tienden a obtener mejor `user_score`.
2. El `esrb_rating` influye en la percepcion del usuario (M y T con mayor media).
3. El genero y la plataforma explican diferencias sistematicas en `user_score`.

## 6. Riesgos y Limitaciones
- Missing significativo en `user_score` y `meta_score`.
- Variables categoricas libres (genres/developers) requieren preprocesamiento.

## 7. Proximos Pasos
- Preparar features (encoding de categoricas, parsing de fecha, limpieza de `genres`).
- Entrenar baseline (regresion lineal) y mejora (RandomForest).

---

**Figuras generadas**:
- `reports/figures/dist_user_score.png`
- `reports/figures/dist_meta_score.png`
- `reports/figures/corr_heatmap_numeric.png`
