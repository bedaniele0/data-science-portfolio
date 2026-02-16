# Data Quality Report - Prediccion de User Score

Autor: Ing. Daniel Varela Perez
Email: bedaniele0@gmail.com
Tel: +52 55 4189 3428
Fecha: 2026-02-06
Version: 1.0

---

## 1. Dataset Overview
- Fuente: data.csv
- Periodo: 1996-09-26 a 2021-02-12
- Filas: 1026
- Columnas: 9

## 2. Missing Values
| Columna | % Missing | Accion |
|---|---|---|
| meta_score | 35.58% | imputar |
| user_score | 24.27% | imputar |
| esrb_rating | 11.31% | imputar |
| developers | 1.17% | imputar |
| genres | 0.88% | imputar |
| date | 0.00% | sin accion |
| platform | 0.00% | sin accion |
| title | 0.00% | sin accion |
| link | 0.00% | sin accion |

## 3. Duplicados
- Total duplicados: 0
- Accion: No se eliminan (0 duplicados)

## 4. Outliers
- Metodo: IQR
- Columnas afectadas: meta_score (9), user_score (30)
- Accion: Revisar impacto, considerar winsorizacion si afecta MAE/R2

## 5. Consistencia y Reglas
| Regla | Resultado | Notas |
|---|---|---|
| `user_score` en rango 0-10 | OK (min 2.0, max 9.7) | Sin valores fuera de rango |
| `meta_score` en rango 0-100 | OK (min 37, max 99) | Sin valores fuera de rango |

## 6. Issues Abiertos
| ID | Issue | Severidad | Accion | Owner |
|---|---|---|---|---|
| Q1 | Missing en `user_score` (24.3%) | Media | Imputar o filtrar | DS |
| Q2 | Missing en `meta_score` (35.6%) | Media | Imputar o usar modelo con missing | DS |
