# Data Quality Report - Credit Risk Scoring (UCI Taiwan)

**Autor:** Ing. Daniel Varela Perez  
**Email:** bedaniele0@gmail.com  
**Fecha:** 2026-02-04  
**Versión:** 1.0

---

## 1. Resumen
- Dataset: 30,000 registros, 25 variables.
- Missing: 0%.
- Duplicados: 0.
- Desbalance: 22.12% default (3.52:1).
- Issues: valores inconsistentes en `EDUCATION` y `MARRIAGE`.

## 2. Controles de Calidad
| Check | Resultado | Evidencia |
|---|---|---|
| Missing values | 0% | `df.isnull().sum().sum() == 0` |
| Duplicados | 0 | `df.duplicated().sum() == 0` |
| Rangos | OK | `AGE 21-79`, `PAY_* -2..8`, `BILL_AMT* >= -165,580` |
| Valores categóricos | Parcial | `EDUCATION` y `MARRIAGE` con códigos no documentados |

## 3. Riesgos de Calidad
- **Temporal:** Dataset 2005 (posible drift).
- **Codificación:** categorías no documentadas en `EDUCATION`, `MARRIAGE`.
- **Moneda:** montos en NT$ (necesario documentar en model card).

## 4. Acciones Correctivas
1. Agrupar `EDUCATION` (0,5,6 → 4).
2. Agrupar `MARRIAGE` (0 → 3).
3. Validación automática futura con Great Expectations.

## 5. Conclusión
Calidad general **alta** con issues menores corregibles mediante feature engineering.

---

**© 2026 - DVP-MASTER Framework - Ing. Daniel Varela Perez**
