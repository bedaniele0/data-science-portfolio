# Data Sources

**Proyecto:** Credit Risk Scoring (UCI Taiwan)  
**Fecha:** 2026-02-04

## 1. Inventario de fuentes
| Fuente | Tipo | Owner | Ubicación | Frecuencia | Descripción |
|---|---|---|---|---|---|
| UCI Taiwan Default (2005) | CSV/XLS | UCI ML Repository | `data/raw/default of credit card clients.csv` | Estática | Dataset histórico de default |

## 2. Esquemas clave
- UCI Default 2005 → `docs/04_data_contract.md`

## 3. Calidad y riesgos
- Dataset histórico (2005): riesgo de drift temporal.
- Variables codificadas (EDUCATION/MARRIAGE): requiere mapeo/agrupación.

## 4. Acceso y cumplimiento
- Método de acceso: archivo local en repo.
- PII: No (datos anonimizados).
- Retención: N/A (dataset público).

## 5. Validación mínima automatizable
- Verificar esquema y columnas esperadas.
- Validar rangos (AGE, SEX, PAY_*, montos).
- Verificar duplicados en `ID`.
