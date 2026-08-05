# Architecture

```text
raw sources -> ingestion -> normalized articles -> relevance -> clustering -> master SQLite -> serving contract -> dashboard contract -> API/dashboard
```

## Componente 1: Ingestion

Responsabilidades:

- leer fuentes externas;
- validar columnas disponibles;
- normalizar texto, fechas, medios y URLs;
- crear identificadores reproducibles;
- remover duplicados exactos;
- emitir un reporte de calidad.

Contrato principal: `src/ingestion/schema.py`.

## Componente 2: Relevance Filtering

Responsabilidades:

- aplicar reglas configurables de evento y actor;
- producir scores auditables por articulo;
- separar articulos candidatos para clustering;
- generar reporte de cobertura;
- calcular metricas supervisadas cuando existan etiquetas humanas.

El baseline actual no pretende ser el modelo final. Su valor es crear una referencia estable y explicable para compararla contra modelos NLP posteriores.

## Componente 3: Event Clustering

Responsabilidades:

- convertir articulos relevantes en grupos de evento;
- usar similitud textual y cercania temporal como baseline;
- generar `events` y `article_event_links` como base relacional inicial;
- separar eventos dudosos en una cola de revision humana.

Este baseline no sustituye la revision editorial. Su objetivo es crear una primera agrupacion reproducible y medible para comparar contra embeddings y modelos de pares en fases posteriores.

## Validation Harness

El proyecto integra validacion automatica en `Makefile`:

- `make test`: pruebas unitarias e integracion.
- `make validate-artifacts`: existencia y estructura minima de artefactos.
- `make validate-notebooks`: ejecucion completa de notebooks con `nbmake`.
- `make validate`: compuerta completa para avanzar de componente.

Los notebooks son entregables ejecutables. Si no corren de punta a punta, no estan terminados.

## Componente 4: Master SQLite Database

Responsabilidades:

- consolidar artefactos CSV en una base relacional SQLite;
- crear tablas consumibles por API y dashboard;
- registrar una corrida en `pipeline_runs`;
- emitir un reporte de conteos y ubicacion de base.

La base `data/processed/events.db` es el contrato operativo para los componentes de producto.


## Componente 5: Serving Query Layer

Responsabilidades:

- encapsular consultas contra `data/processed/events.db`;
- exponer endpoints FastAPI para salud, eventos, detalle de evento, articulos por evento, cola de revision y busqueda;
- validar el contrato de serving con un pipeline reproducible;
- dejar un reporte auditable en `reports/serving_contract_report.json`.

Esta capa desacopla los consumidores de producto de los artefactos internos del pipeline. El dashboard futuro debe consumir `src.serving.queries` o la API, no leer CSVs directamente.


## Componente 6: Dashboard Streamlit

Responsabilidades:

- presentar KPIs ejecutivos sobre articulos, eventos y cola de revision;
- visualizar estado de eventos y cobertura por medio;
- permitir busqueda y revision de articulos vinculados;
- consumir la capa `src.serving.queries` como contrato estable;
- validar el snapshot del dashboard antes de considerarlo entregable;
- reconciliar automaticamente los KPI visibles contra `data/processed/events.db` y fallar si los numeros mostrados no coinciden con la fuente procesada.

El dashboard es una capa de producto sobre el sistema de ciencia de datos, no una fuente de logica del pipeline.
