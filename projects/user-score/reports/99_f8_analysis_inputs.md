# Inputs F8 Analisis Continuo - Prediccion de User Score

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

## 2. Ventana de Analisis
- Periodo: semanal y mensual (rolling)
- Frecuencia: semanal (performance) + mensual (negocio)

## 3. Datos Disponibles
- Features de produccion: si (batch input) (SIMULADO)
- Predicciones guardadas: si
- Labels reales: si, con delay 7-14 dias

## 4. Fuente de Labels y Union
- Fuente de labels: tabla `actual_user_score`
- Llave de union: id + event_date
- Fallback: join por id cuando labels llegan tarde

## 5. Metricas Tecnicas Objetivo
- MAE <= 0.60
- R2 >= 0.50
- PSI warning > 0.20 / critical > 0.30
- MAE +10% warning / +20% critical
- R2 -0.05 warning / -0.10 critical

## 6. KPIs de Negocio
- Anticipar percepcion del usuario
- Drivers de user_score documentados

## 7. Fuentes y Ubicaciones
- Input batch: `s3://NO_DEFINIDO/user_score/prod/input/dt=YYYY-MM-DD/input.csv`
- Predicciones: `s3://NO_DEFINIDO/user_score/prod/predictions/dt=YYYY-MM-DD/predictions.csv`
- Labels: `s3://NO_DEFINIDO/user_score/prod/actuals/dt=YYYY-MM-DD/actuals.csv`
- Monitoreo: `s3://NO_DEFINIDO/user_score/prod/monitoring/dt=YYYY-MM-DD/`

## 8. Observaciones
- Dataset con missing en user_score y meta_score.
- Reentrenamiento mensual o por drift critico.

---

**© 2026 - DVP-MASTER Framework - Ing. Daniel Varela Perez**
