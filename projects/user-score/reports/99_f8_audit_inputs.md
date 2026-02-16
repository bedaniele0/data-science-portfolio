# Inputs F8 Auditoria - Prediccion de User Score

**Autor**: Ing. Daniel Varela Perez
**Email**: bedaniele0@gmail.com
**Tel**: +52 55 4189 3428
**Fecha**: 19/01/2026
**Framework**: DVP-MASTER v2.0

---

## 1. Proyecto / Modelo
- Nombre del modelo/proyecto: proyecto_user_score_ds
- Tipo de problema: Regresion
- Canal de despliegue: Batch diario
- Version actual: v1.0

## 2. Ventana de Auditoria
- Periodo a auditar: 30 dias (rolling)
- Frecuencia de revision: mensual

## 3. Datos Disponibles
- Training set original: si (`data/data.csv`)
- Logs de produccion: batch logs (scheduler) (SIMULADO)
- Predicciones guardadas: si (S3, `predictions_user_score`)
- Labels reales: si (S3, `actual_user_score`, delay 7-14 dias)

## 4. Fuentes y Ubicaciones
- Input batch: `s3://NO_DEFINIDO/user_score/prod/input/dt=YYYY-MM-DD/input.csv`
- Predicciones: `s3://NO_DEFINIDO/user_score/prod/predictions/dt=YYYY-MM-DD/predictions.csv`
- Labels: `s3://NO_DEFINIDO/user_score/prod/actuals/dt=YYYY-MM-DD/actuals.csv`
- Monitoreo: `s3://NO_DEFINIDO/user_score/prod/monitoring/dt=YYYY-MM-DD/`

## 5. Llaves de Union
- Primary: id
- Secundaria: event_date (o date_window equivalente)
- Fallback: join por id cuando labels llegan con delay

## 6. Metricas Objetivo (F0)
- MAE <= 0.60
- R2 >= 0.50
- RMSE: minimizar

## 7. KPIs de Negocio
- Anticipar percepcion del usuario
- Identificar drivers de user_score para decisiones de mejora

## 8. Observaciones
- Datos sin sensibilidad personal
- Drift esperado en genres/plataformas

---

**© 2026 - DVP-MASTER Framework - Ing. Daniel Varela Perez**
