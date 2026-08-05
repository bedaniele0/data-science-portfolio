# Data Dictionary

## articles normalized

- `article_id`: identificador estable derivado de URL o contenido.
- `source`: origen logico de la ingesta.
- `query`: consulta inferida desde `search_URL` cuando existe.
- `title`: titulo normalizado.
- `description`: descripcion normalizada.
- `published_at`: fecha de publicacion en formato ISO.
- `media`: medio normalizado.
- `url`: URL canonica si existe.
- `raw_text`: concatenacion de titulo y descripcion para features posteriores.
- `content_hash`: hash estable del contenido principal.
- `ingested_at`: timestamp UTC de la corrida.

## scored_articles

Incluye todas las columnas normalizadas de `articles` mas:

- `is_relevant`: bandera baseline para pasar a agrupacion.
- `relevance_score`: score heuristico del baseline.
- `matched_event_terms`: grupos de evento detectados.
- `matched_actor_terms`: grupos de actor detectados.
- `has_event_terms`: bandera auxiliar.
- `has_actor_terms`: bandera auxiliar.

## events

- `event_id`: identificador estable del cluster.
- `event_number`: numero secuencial de evento en la corrida.
- `event_title`: titulo representativo.
- `first_date`: primera fecha observada.
- `last_date`: ultima fecha observada.
- `article_count`: numero de notas vinculadas.
- `media_count`: numero de medios distintos.
- `query_count`: numero de consultas distintas que alimentaron el evento.
- `confidence`: confianza promedio del cluster.
- `status`: `auto` o `needs_review`.
- `example_article_id`: articulo representativo.
- `example_url`: URL representativa.

## article_event_links

- `event_id`: evento consolidado.
- `article_id`: nota vinculada.
- `link_confidence`: similitud maxima de la nota contra otro miembro del evento.
- `title`, `media`, `published_at`, `url`: contexto para revision.

## cluster_review

Eventos que requieren revision humana por tener una sola nota o baja confianza de cluster.

## pipeline_runs

- `run_id`: identificador unico de corrida.
- `run_started_at`: timestamp UTC.
- `source`: origen logico de la corrida.
- `articles_rows`, `scored_articles_rows`, `events_rows`, `article_event_links_rows`, `review_queue_rows`: conteos cargados a SQLite.


## serving_contract_report

- `database_path`: ruta de la base consultada.
- `table_counts`: conteos de tablas requeridas por la capa de serving.
- `events_returned`: numero de eventos devueltos por la consulta principal.
- `review_queue_returned`: numero de filas devueltas para revision humana.
- `search_text`: texto usado en la prueba de busqueda.
- `search_results_returned`: resultados encontrados por la busqueda smoke.
- `top_event_id`: evento usado para validar detalle y articulos.
- `top_event_article_count`: articulos vinculados al evento principal.
- `contract_checks`: banderas booleanas de salud funcional del contrato.


## dashboard_contract_report

- `database_path`: ruta de la base consumida por el dashboard.
- `table_counts`: conteos de tablas disponibles.
- `events_returned`: eventos disponibles para la vista principal.
- `review_queue_returned`: eventos devueltos para revision humana.
- `media_coverage_returned`: medios incluidos en la grafica de cobertura.
- `search_text`: texto usado para la prueba smoke de busqueda.
- `search_results_returned`: resultados devueltos por la busqueda smoke.
- `top_event_id`: evento seleccionado para validar detalle.
- `top_event_article_count`: articulos vinculados al evento principal.
- `dashboard_checks`: banderas booleanas del contrato funcional del dashboard.
