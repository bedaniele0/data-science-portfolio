# EDA Report - Credit Risk Scoring (UCI Taiwan)

**Autor:** Ing. Daniel Varela Perez  
**Email:** bedaniele0@gmail.com  
**Fecha:** 2026-02-04  
**Versión:** 1.0

---

## 1. Resumen Ejecutivo
El dataset UCI Taiwan (30,000 registros, 25 variables) presenta un **default rate de 22.12%** con un desbalance moderado (3.52:1). Las variables de comportamiento de pago (`PAY_*`) muestran la mayor correlación con el target. Se identificaron inconsistencias en `EDUCATION` y `MARRIAGE` que requieren agrupación.

## 2. Distribución del Target
- **No Default (0):** 23,364 (77.88%)
- **Default (1):** 6,636 (22.12%)
- **Imbalance ratio:** 3.52:1

## 3. Hallazgos Clave

### 3.1 Variables más correlacionadas con el target
Top 5 por correlación:
1. **PAY_0** (0.324)
2. **PAY_2** (0.264)
3. **PAY_3** (0.235)
4. **PAY_4** (0.218)
5. **PAY_5** (0.205)

### 3.2 Demografía vs Default
**Sexo**
- Male: 39.6% de la base, default rate 23.5%
- Female: 60.4% de la base, default rate 21.4%

**Educación**
- Graduate: 35.3% (default 21.2%)
- University: 46.8% (default 22.8%)
- High School: 16.4% (default 22.0%)
- Other: 1.5% (default 23.5%)

**Estado civil**
- Married: 45.5% (default 20.8%)
- Single: 53.2% (default 23.2%)
- Other: 1.3% (default 23.3%)

**Edad**
- 21-25: 10.9% (default 25.4%)
- 26-35: 40.1% (default 23.6%)
- 36-45: 30.9% (default 20.5%)
- 46-60: 16.1% (default 19.2%)
- 60+: 1.9% (default 17.5%)

## 4. Problemas de Calidad Detectados
- **EDUCATION** contiene valores {0,5,6} no documentados.
- **MARRIAGE** contiene valor 0 no documentado.
- Montos de `BILL_AMT*` pueden ser negativos (crédito a favor).

## 5. Acciones Recomendadas
1. Agrupar `EDUCATION` (0,5,6 → 4).
2. Agrupar `MARRIAGE` (0 → 3).
3. Aplicar balanceo de clases (class weighting o SMOTE).
4. Monitorear drift en `PAY_0`, `LIMIT_BAL`, `utilization_1`.

## 6. Evidencia
- Notebook ejecutado: `notebooks/01_eda.ipynb`
- Reporte de calidad: `docs/06_data_quality_report.md`

---

**© 2026 - DVP-MASTER Framework - Ing. Daniel Varela Perez**
