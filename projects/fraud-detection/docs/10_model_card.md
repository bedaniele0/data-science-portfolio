# 10 - Model Card (Fraud Detection)

- Project: `fraud_detection`
- Owner: `Ingeniero Daniel Varela Perez / S. Data Science`
- Model: `RandomForest/Thresholded` (best_model.pkl)
- Version: `1.0.0`
- Date: `2026-02-05`

## Summary

Binary classifier to detect fraudulent transactions (UCI Credit Card Fraud dataset).

## Data

- Source: `data/raw/creditcard.csv`
- Target: `Class` (1 = fraud)
- Imbalance: ~0.17% fraud

## Performance (Test)

- AUC: 0.9437
- Precision: 0.8442
- Recall: 0.6633
- F1: 0.7429

## Artifacts

- Model: `models/best_model.pkl`
- Metrics: `reports/metrics/validation_results.json`
