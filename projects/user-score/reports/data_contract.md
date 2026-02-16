# Data Contract - Prediccion de User Score

Autor: Ing. Daniel Varela Perez
Email: bedaniele0@gmail.com
Tel: +52 55 4189 3428
Fecha: 2026-02-06
Version: 1.0

---

## 1. Objetivo
Definir el esquema y reglas de datos para el pipeline batch de prediccion de user_score.

## 2. Tabla de Entrada (batch diario)
**Nombre logico**: input_user_score_batch
**Storage**: S3 (path particionado por fecha)
**Ejemplo**: `s3://user-score-mlops-bucket/user_score/prod/input/dt=YYYY-MM-DD/input.csv`

| Campo | Tipo | Requerido | Regla |
|---|---|---|---|
| id | string | si | Identificador unico de registro |
| title | string | no | Nombre del juego |
| platform | string | si | Plataforma (ej. PS4, Switch, iOS) |
| date | string (YYYY-MM-DD) | si | Fecha de lanzamiento |
| meta_score | float | no | Score de critica (0-100) |
| esrb_rating | string | no | Clasificacion ESRB |
| developers | string | no | Desarrollador/es |
| genres | string | si | Lista en formato ['Action','3D'] |

**Frecuencia**: diaria (snapshot T-1)

## 3. Tabla de Salida (predicciones)
**Nombre logico**: predictions_user_score
**Storage**: S3 (path particionado por fecha)
**Ejemplo**: `s3://user-score-mlops-bucket/user_score/prod/predictions/dt=YYYY-MM-DD/predictions.csv`

| Campo | Tipo | Requerido | Regla |
|---|---|---|---|
| id | string | si | Mismo id de entrada |
| prediction_date | string (YYYY-MM-DD) | si | Fecha de batch |
| predicted_user_score | float | si | Score predicho (0-10) |
| model_version | string | si | Version del modelo (v1.0) |
| features_hash | string | si | Hash del vector de features |

## 4. Tabla de Labels Reales
**Nombre logico**: actual_user_score
**Storage**: S3 (path particionado por fecha)
**Ejemplo**: `s3://user-score-mlops-bucket/user_score/prod/actuals/dt=YYYY-MM-DD/actuals.csv`

| Campo | Tipo | Requerido | Regla |
|---|---|---|---|
| id | string | si | Mismo id de entrada |
| event_date | string (YYYY-MM-DD) | si | Fecha de label real |
| real_user_score | float | si | Score real (0-10) |

## 5. Llave de Union
- Primary: id
- Secundaria: event_date (o date_window equivalente)
- Nota: si labels llegan con delay, se permite join por id mientras se alinea ventana temporal.

## 6. Validaciones Basicas
- `user_score` y `meta_score` en rango valido.
- `date` parseable en formato ISO.
- `genres` con formato lista.

## 7. Manejo de Cambios
- Cualquier cambio de schema debe notificarse con 1 semana de anticipacion.
- Cambios en `genres` o `platform` generan alertas de drift.

---

**© 2026 - DVP-MASTER Framework - Ing. Daniel Varela Perez**
