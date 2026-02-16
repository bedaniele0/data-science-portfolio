# 11 - Runbook Operativo (Fraud API)

- Project: `fraud_detection`
- Owner: `Ingeniero Daniel Varela Perez / S. Data Science`
- Date: `2026-02-05`

## Service Overview

- API: `api/`
- Deployment: `Dockerfile`

## Start / Stop

```bash
# API
Docker build -t fraud-api:latest -f Dockerfile .
Docker run -p 8000:8000 fraud-api:latest
```

## Health Checks

- `GET /health`
- Expected: `status=healthy`

## Model Artifacts

- `models/best_model.pkl`
- `models/threshold_config.json`

## Monitoring Signals

- Latency p95
- Error rate
- Drift score (PSI/KS)

## Rollback

1. Revert Docker image tag
2. Restore `models/best_model.pkl` from last known good build
