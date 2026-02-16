# Case Study (1 Page): Fraud Detection System (E2E)

## 1) Problema
Un equipo de riesgo necesitaba detectar transacciones fraudulentas en tiempo casi real. El reto principal no era solo "clasificar bien", sino reducir costo operativo:
- Un falso negativo (fraude no detectado) tiene costo alto.
- Un falso positivo excesivo bloquea operaciones legítimas y afecta experiencia de cliente.

Adicionalmente, el modelo debía ser consumible por otras aplicaciones de negocio con una interfaz estable (API) y con visualización para análisis (dashboard).

## 2) Decisión técnica clave
La decisión principal fue optimizar el sistema por utilidad operativa, no solo por métrica global.

Se implementó:
- Pipeline reproducible de entrenamiento y evaluación con separación estricta train/test.
- Comparación de modelos y selección basada en AUC + equilibrio Precision/Recall.
- Ajuste de umbral orientado a costo FN/FP (en vez de usar 0.5 por defecto).
- Exposición vía FastAPI (servicio de predicción) y Streamlit (consumo para negocio).

Por qué esta decisión:
- En fraude, maximizar AUC sin política de umbral no garantiza impacto económico.
- Umbral por costo conecta directamente el modelo con decisiones de operación.

## 3) Impacto
Resultados del proyecto:
- AUC: 0.9528
- Precision: 0.9362
- Recall: 0.7213
- F1: 0.8148

Impacto de negocio (escenario demo):
- Ahorro potencial: ~$25.9M/año
- Escenario conservador: ~$7.8M/año

Resultado para portafolio:
- Proyecto E2E demostrable (datos -> modelo -> API -> dashboard).
- Caso sólido para entrevistas: muestra criterio técnico + traducción a impacto económico.
