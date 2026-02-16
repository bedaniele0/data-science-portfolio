# F0 Checklist Validation

Fecha: 2026-02-04  
Proyecto: Credit Risk Scoring (UCI Taiwan)

## Resumen
- Estado general: ✅ COMPLETADO
- Notas: F0 actualizado con templates DVP-MASTER y baseline cuantitativo.

## Checklist
- [x] Problema definido en 2-3 oraciones.
- [x] KPI de negocio definido.
- [x] KPI tecnico definido.
- [x] Baseline cuantitativo definido (mean/median/naive).
- [x] Dataset identificado (A/B/C).
- [x] Restricciones documentadas.
- [x] Sponsor confirmado.
- [x] Tamano S/M/L justificado (2-3 bullets).

## Evidencia
- `docs/01_problem_statement.md`
- `docs/02_kpi_tree.md`
- `docs/03_business_case.md`
- `data/raw/default of credit card clients.csv`
- `data/raw/default of credit card clients.xls`
- `data/processed/credit_data_processed.csv`
- `data/processed/featured_dataset.csv`

## Dataset A/B/C
- **A (Raw)**: `data/raw/default of credit card clients.csv` / `.xls`
- **B (Processed)**: `data/processed/credit_data_processed.csv`
- **C (Featured/Model-ready)**: `data/processed/featured_dataset.csv`

## Baseline cuantitativo
- Default rate base (raw): **22.12%** (n=30,000)
- Baseline técnico: AUC 0.50 (random), KS 0.00

## Tamaño del proyecto (M)
- Dataset tabular mediano (30k filas, 25 variables).
- Modelo supervisado con restricciones de explicabilidad y fairness.
- Impacto de negocio significativo, pero sin infraestructura en tiempo real compleja.
