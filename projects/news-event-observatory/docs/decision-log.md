# Decision Log

## 2026-08-04: SQLite como base inicial

Se usara SQLite en el MVP para evitar infraestructura prematura y mantener trazabilidad local. El esquema se disenara para migrar a PostgreSQL si el proyecto crece.

## 2026-08-04: Datos demo como semilla

Los datos del flujo exploratorio previo se usaran solo para bootstrap, pruebas y evaluacion inicial. La fuente operativa futura sera el pipeline propio.

## 2026-08-04: Ingesta antes que modelo

Primero se implementa contrato de datos e ingesta reproducible. El modelo de relevancia y clustering queda bloqueado hasta tener datos normalizados y muestra etiquetable.

## 2026-08-04: Reglas explicables como baseline de relevancia

El componente 2 inicia con reglas auditables derivadas de Dedup/relevant_events.R. No se entrena ML hasta contar con etiquetas humanas suficientes para medir precision, recall y F1.

## 2026-08-04: TF-IDF temporal como baseline de clustering

El componente 3 inicia con TF-IDF, similitud coseno y ventana temporal. La prioridad es tener una agrupacion explicable y reproducible antes de usar embeddings o modelos supervisados de pares.

## 2026-08-04: Base maestra SQLite como contrato operativo

El componente 4 consolida CSVs en SQLite para que API y dashboard lean una fuente relacional estable. PostgreSQL queda reservado para crecimiento o concurrencia multiusuario.


## 2026-08-04 - Serving antes de dashboard

Decision: construir una capa de consulta y API FastAPI antes del dashboard.

Motivo: el dashboard de portafolio debe consumir un contrato estable sobre SQLite y no acoplarse a CSVs intermedios. Esto mejora mantenibilidad, pruebas automatizadas y claridad de arquitectura ML engineering.


## 2026-08-04 - Dashboard como capa de producto validada

Decision: construir el dashboard Streamlit sobre `src.serving.queries` y agregar un pipeline de contrato antes de abrirlo como entregable.

Motivo: mantener separada la logica de datos de la interfaz, permitir pruebas automatizadas y conservar la reproducibilidad del ecosistema de ciencia de datos.
