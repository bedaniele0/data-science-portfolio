# 14 - Monitoring Runbook (F8)

- Project: `fraud_detection`
- Owner: `Ingeniero Daniel Varela Perez / S. Data Science`
- Date: `2026-02-05`

## Signals & Thresholds

- PSI avg: GREEN < 0.10 | YELLOW 0.10–0.20 | RED > 0.20
- PSI max feature: GREEN < 0.20 | YELLOW 0.20–0.25 | RED > 0.25
- KS score drift: GREEN < 0.10 | YELLOW 0.10–0.20 | RED > 0.20
- Latency p95: GREEN < 150 ms | YELLOW 150–300 ms | RED > 300 ms

## Frequency

- Weekly drift monitoring (batch)
- Daily latency/error checks (if running in production)

## Actions

- GREEN: continue monitoring
- YELLOW: investigate top drifting features, validate data pipeline
- RED: trigger optimization (MO), retrain if confirmed
