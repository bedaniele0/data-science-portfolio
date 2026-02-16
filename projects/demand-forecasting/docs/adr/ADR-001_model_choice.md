# ADR-001: Elección de modelo principal (LightGBM) para forecasting tabular

**Autor:** Ing. Daniel Varela Perez  
**Email:** bedaniele0@gmail.com  
**Tel:** +52 55 4189 3428  
**Fecha:** 13 de Diciembre, 2024  
**Estado:** Aprobado  

## Contexto
El problema requiere pronosticar demanda diaria de 30k+ series (item-tienda) con features tabulares (lags, rolling, calendario, precios, eventos). Se necesita alta precisión, entrenamiento rápido y explicabilidad razonable. El stack debe ejecutarse en entorno batch y servir predicciones en API.

## Decisión
Usar **LightGBM Regressor** como modelo principal para forecasting a nivel de SKU-tienda.

## Justificación
- Rendimiento superior en datos tabulares con interacciones no lineales y alta cardinalidad.
- Manejo nativo de valores faltantes y capacidad para dataset amplio (millones de filas) con buen tiempo de entrenamiento.
- Importancias de variables accesibles para storytelling y monitoreo.
- Fácil ajuste de hiperparámetros y soporte para `categorical_feature` si se requiere.
- Infraestructura simple: entrenamiento offline, scoring rápido en CPU (<100 ms p95 en API con feature base en memoria).

## Alternativas consideradas
- **XGBoost**: rendimiento similar pero mayor sensibilidad a tuning y tiempos más largos en CPU para dataset completo.
- **Prophet/ARIMA**: mejor para series univariadas, no escala a 30k series con múltiples features y relaciones cruzadas.
- **Redes recurrentes (LSTM/GRU)**: complejidad y tiempo de entrenamiento mayores, explicabilidad menor; descartado para MVP.

## Consecuencias
- Se requiere mantener el orden y nombres de features para inferencia; se incluyó `feature_importance_lgb.csv` como respaldo.
- Necesidad de monitorear drift y recalibrar hiperparámetros periódicamente.
- Se facilita el despliegue ligero (joblib + FastAPI), sin dependencias de GPU.
