# Problem Statement - Sistema Inteligente de Detección de Fraude
Autor: Ing. Daniel Varela Perez  
Email: bedaniele0@gmail.com  
Tel: +52 55 4189 3428  
Metodología: DVP-PRO (Fase 0)

## 1. Contexto de Negocio
Un procesador de pagos B2B procesa ~120M transacciones/año para comercios en LATAM. El fraude histórico oscila entre 0.15% y 0.25% del volumen, con pérdidas financieras, contracargos y riesgo reputacional. El objetivo es reducir fraude y minimizar falsos positivos que afecten conversión.

## 2. Problema a Resolver
Detectar transacciones potencialmente fraudulentas en tiempo (quasi) real con un modelo ML y exponerlo vía API y dashboard. El sistema debe permitir ajustar el umbral de decisión para balancear recall vs. false positives según la tolerancia de negocio.


## 2.1 Problem Statement (2–3 sentences)
El fraude en pagos B2B es bajo en tasa pero alto en impacto, y los sistemas basados solo en reglas generan falsos positivos que afectan la conversión. Se requiere un modelo ML que detecte fraude en casi tiempo real con alta precisión y recall, manteniendo la latencia bajo control. El objetivo es reducir pérdidas por contracargos sin deteriorar la experiencia del cliente.


## 2.2 Baseline cuantitativo
- **Naive (all non-fraud)**: Recall fraude = 0.00, AUC = 0.50.
- **Fraud rate histórico**: 0.15%–0.25% (≈0.2%).


## 2.3 Dataset A/B/C (Obligatorio)
- **A (raw)**: `data/raw/creditcard.csv`
- **B (processed train/val/test)**: `data/processed/train_clean.parquet`, `data/processed/validation_clean.parquet`, `data/processed/test_clean.parquet`
- **C (demo/serving)**: `data/processed/demo/`

## 3. Objetivos Específicos (medibles)
- Recall (fraude) >= 0.85 en test y producción inicial.
- FPR <= 0.02 para no deteriorar conversión.
- Latencia P95 de predicción (API) <= 150 ms en modo online.
- Throughput mínimo: 1000 tx/s en batch offline (CLI o job programado).
- Drift monitorizado diariamente (PSI <= 0.2 en variables clave).

## 4. Métricas de Éxito (negocio y técnicas)
- Negocio: reducir contracargos en 20-30% Y/Y, payback < 6 meses.
- Conversión: mantener tasa de aprobación > 97.5%.
- Operación: uptime API >= 99.5%, tiempo medio de respuesta P95 <= 150 ms.
- ML: Recall >= 0.85, Precision >= 0.75, AUC >= 0.95; MAPE de tasa de fraude <= 10% en monitoreo.

## 5. Stakeholders
- Sponsor: VP de Riesgos.
- Usuarios finales: analistas antifraude y equipo de operaciones.
- Equipo técnico: Data Science, Data Engineering, MLOps, Seguridad.
- Integradores: equipos de producto/API de comercios.

## 6. Restricciones y Supuestos
- Datos: altamente desbalanceados; datos sensibles deben pasar por PII hashing y cumplimiento GDPR/CCPA.
- Infra: ejecución en contenedores; sin dependencias de GPU.
- Operación: ventanas batch disponibles fuera de picos; límites batch <= 1000 filas por request en API batch.
- Seguridad: auth obligatoria (JWT/API key); logs sin PII en claro.

## 7. Alcance y Fuera de Alcance
- En alcance: scoring online/batch, dashboard de monitoreo, alertas básicas de drift y tasa de fraude.
- Fuera de alcance (versión actual): reglas expertas dinámicas, orquestación multi-región activa-activa, feature store online.

## 8. Criterios de Aceptación (Fase 0)
- Documentación de métricas de éxito y ROI estimado aprobada por sponsor.
- Contrato de datos y esquema de entrada validados con Ingeniería.
- Objetivos técnicos y de negocio trazados en roadmap y en arquitectura técnica.

## 9. Timeline Tentativo
- Semana 1-2: cierre F0-F2 (problem statement, arquitectura, datos base).
- Semana 3-4: EDA/FE y baseline + tuning.
- Semana 5: API + dashboard + pruebas.
- Semana 6: monitoreo y handover.

## 10. Riesgos y Mitigaciones
- Desbalance extremo: usar threshold tuning, class weights y evaluación focalizada en recall/FPR.
- Drift de distribución: monitoreo PSI/K-S y plan de retraining mensual o bajo alerta.
- Latencia: pre-carga de modelo y validación de payloads; batch limitado.
- Privacidad: anonimización previa y control de acceso estrictos.

## 11. Decision Logs / Próximos Pasos
- Validar con negocio el trade-off recall vs. FPR y fijar umbral operativo inicial.
- Acordar frecuencia de retraining y ventana de datos.
- Confirmar SLO de latencia y throughput para sizing de infraestructura.
