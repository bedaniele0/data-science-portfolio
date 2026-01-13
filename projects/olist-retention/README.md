# Olist Customer Retention Analytics (E2E)

**One-liner:** Analítica end-to-end de retención para e-commerce (cohortes, RFM y CLV) con entrega en dashboard y/o API para toma de decisiones.  
**Stack:** Python, pandas, SQL (si aplica), Streamlit (si aplica), FastAPI (si aplica).  
**Deliverable:** Reporte analítico reproducible + Dashboard (y API si aplica).  
**Results:** <completa: 2–3 KPIs clave, ej. retención por cohortes, segmentos RFM, CLV estimado>.

## Problem
Entender y mejorar la retención de clientes en un e-commerce: identificar patrones de recompra, segmentar clientes y priorizar acciones (CRM/promos) basadas en valor y probabilidad de retorno.

## Data
- Source: Olist / Kaggle (si aplica)
- Size: <completa: #orders, #customers, periodo>

## Approach
- Cohort analysis para medir retención por mes de primera compra.
- Segmentación **RFM** (Recency, Frequency, Monetary) para activar campañas por tipo de cliente.
- Estimación de **CLV** (aprox.) y/o priorización de clientes de alto valor para acciones de retención.

## Results
- Metric(s): <completa: retención, repeat rate, CLV, % clientes por segmento>
- Key insight: Los segmentos RFM permiten mover acciones de “masivas” a “priorizadas” (alto valor vs riesgo de churn).

## Demo
- Dashboard: <link o "local">
- API (si aplica): <link o "local">

## How to run
- Install:
  - `pip install -r requirements.txt`
- Run (si aplica):
  - `streamlit run app/app.py`
  - `uvicorn app.main:app --reload`

## Repo structure
- `src/` lógica de datos/análisis
- `app/` dashboard y/o API
- `reports/` figuras y resultados
- `data/` (si aplica; ideal: no subir datos pesados)

## Next steps
- Agregar métricas de producto (repeat purchase window, time-to-second-purchase).
- Experimentación: propuesta de A/B test para campañas por segmento RFM.
