# Drift Interpretation Guide (F8)

- Project: `fraud_detection`
- Owner: `Ingeniero Daniel Varela Perez / S. Data Science`
- Date: `2026-02-05`

## Purpose

Interpret drift signals (PSI/KS) and define response actions.

## Metrics

- **PSI (Population Stability Index)**
  - < 0.10: stable (GREEN)
  - 0.10–0.20: moderate drift (YELLOW)
  - > 0.20: significant drift (RED)

- **KS score drift** (prediction distribution difference)
  - < 0.10: stable (GREEN)
  - 0.10–0.20: moderate drift (YELLOW)
  - > 0.20: significant drift (RED)

## Interpretation

- GREEN: no action, continue monitoring
- YELLOW: investigate top drifting features and data pipeline
- RED: trigger optimization (MO) and consider retraining

## Notes

- Monitoring is simulated for portfolio.
