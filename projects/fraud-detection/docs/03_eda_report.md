# 03 - EDA Report (Fraud Detection)

- Project: `fraud_detection`
- Owner: `Ingeniero Daniel Varela Perez / S. Data Science`
- Date: `2026-02-05`

## Dataset Summary

- Rows: `284807`
- Features: `30` + target `Class`
- Fraud rate: `0.1727%`
- Amount mean/median: `88.35` / `22.0`

## Notes

- Dataset is highly imbalanced (fraud < 1%).
- PCA-transformed features V1–V28 plus `Amount` and `Time`.

## Evidence

- `notebooks/01_sql_eda_analysis.ipynb`
- `reports/sql_eda_results.json`
