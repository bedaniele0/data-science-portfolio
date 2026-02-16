# 04 - Data Contract (Fraud Detection)

- Project: `fraud_detection`
- Owner: `Ingeniero Daniel Varela Perez / S. Data Science`
- Date: `2026-02-05`

## Dataset

- Source: `data/raw/creditcard.csv`
- Target: `Class` (0 = legit, 1 = fraud)
- Records: 284,807 (UCI Credit Card Fraud)

## Schema (raw)

- `Time`: seconds elapsed between each transaction and the first transaction
- `V1` ... `V28`: anonymized PCA components
- `Amount`: transaction amount
- `Class`: target label (fraud)

## Constraints

- No missing values expected
- Class imbalance extreme (~0.17% fraud)
- PII already removed (PCA features)

## Downstream Outputs

- Train/Validation/Test: `data/processed/train_clean.parquet`, `validation_clean.parquet`, `test_clean.parquet`
- Feature scaling: `data/processed/scaler_clean.pkl`
- Pipeline metadata: `data/processed/pipeline_metadata_clean.json`
