# Feature Engineering - Prediccion de User Score

**Autor**: Ing. Daniel Varela Perez  
**Fecha**: 2026-02-06  

## Resumen

Pipeline de features para predicción de `user_score` basado en variables numéricas y categóricas del dataset.

## Transformaciones

- Imputación de faltantes numéricos (median)
- One‑hot encoding de variables categóricas
- Normalización de variables numéricas

## Artefactos

- `reports/feature_importance_top10.csv`
- `reports/genres_vocab.csv`
