# ADR-002: Estrategia de serving y feature store local

**Autor:** Ing. Daniel Varela Perez  
**Email:** bedaniele0@gmail.com  
**Tel:** +52 55 4189 3428  
**Fecha:** 13 de Diciembre, 2024  
**Estado:** Aprobado  

## Contexto
Se necesita servir predicciones en una API REST (FastAPI) para consultas ad hoc y habilitar batch scoring diario. El dataset M5 completo es voluminoso; se deben minimizar latencias y evitar dependencias externas para el portafolio/demo.

## Decisión
- **Feature store local en parquet** (`data/processed/sales_with_features.parquet`) cargado en memoria para inferencia.
- **API FastAPI** con `ModelService` en singleton que:
  - Carga el modelo LightGBM (`models/lightgbm_model.pkl`).
  - Carga la base de features y resuelve filas por `(item_id, store_id, date)` con fallback a última fecha disponible.
- **Batch scoring** mediante scripts en `Makefile` (`predict`, `evaluate`) reutilizando el mismo servicio de features/modelo.

## Justificación
- Parquet + pandas es suficiente para el tamaño actual y permite despliegue portátil (Docker o local) sin servicios administrados.
- Cargar features en memoria reduce latencia de consulta a <100 ms p95 para API.
- Single source of truth de features evita divergencias entre entrenamiento y serving.
- FastAPI provee contratos claros y documentación automática (`/docs`).

## Alternativas consideradas
- **Feast u otro feature store**: mayor robustez, pero overhead de infraestructura no justificado para el alcance de portafolio.
- **Base de datos relacional** (Postgres) para features: más flexible pero agrega latencia y complejidad operativa.
- **Modelo embedido en cliente**: descartado por necesidad de centralizar monitoreo y control de versiones.

## Consecuencias
- Se requiere control de versión de artefactos (parquet + modelo) fuera del repo; recomendado usar DVC/Git LFS.
- El tamaño en memoria debe vigilarse; para escalar, migrar a feature store online/SQL o particionar por tienda.
- El servicio depende de tener la base de features actualizada; agregar job de refresco y validación es crítico (ver monitoreo).
