# Case Study (1 Page): Walmart Demand Forecasting (E2E)

## 1) Problema
El objetivo fue pronosticar demanda por tienda/producto para mejorar planeación de inventario. El reto principal:
- Capturar estacionalidad, eventos y patrones temporales.
- Evitar leakage temporal que infla métricas y falla en operación real.

Además, el resultado debía integrarse como producto demostrable (API + dashboard), no solo como notebook analítico.

## 2) Decisión técnica clave
La decisión central fue priorizar diseño temporal correcto y mejora contra baseline.

Se implementó:
- Feature engineering temporal (lags, rolling statistics, calendario, eventos, precios).
- Backtesting con split temporal consistente.
- Modelo tipo LightGBM para manejar no linealidad y gran volumen.
- Exposición en API y dashboard para uso operativo y revisión rápida de KPIs.

Por qué esta decisión:
- En forecasting, la validación temporal es más crítica que una métrica puntual aislada.
- Mostrar mejora vs baseline comunica valor de negocio de forma clara.

## 3) Impacto
Resultados del proyecto:
- MAE: 0.6845
- RMSE: 3.9554
- MAPE: 52.75%
- Mejora vs baseline: 29.78% en MAE y 33.29% en RMSE

Impacto de negocio (escenario demo):
- ROI estimado: ~$467K/año para 10 tiendas

Resultado para portafolio:
- Proyecto E2E enfocado en forecasting aplicado.
- Evidencia de criterio técnico sólido: validación temporal + traducción a impacto económico.
