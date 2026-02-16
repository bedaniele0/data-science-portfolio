# 10 - Monitoring Report (F8)

- Project: `fraud_detection`
- Owner: `Ingeniero Daniel Varela Perez / S. Data Science`
- Date: `2026-02-05`
- Mode: `SIMULATED`

## Context

- Model: Fraud classifier
- Deployment: FastAPI in Docker
- Reference period: `2025-09-01 to 2025-09-25`
- Current period: `2025-09-26 to 2025-10-10`

## Summary

- Status: **GREEN** (SIMULATED)
- PSI avg: `0.000297`
- PSI max: `0.000636` (`V28`)
- KS score drift: `0.003676`
- Latency p95: `120.0` ms

## Top Drifted Features (PSI)

- `V28`: `0.000636`
- `V1_x_V2`: `0.000592`
- `V22`: `0.000585`
- `V3_x_V4`: `0.000551`
- `V19`: `0.000506`
- `V12`: `0.000479`
- `V13`: `0.000440`
- `V1`: `0.000386`
- `V27`: `0.000371`
- `Time`: `0.000350`


## Decision

- Status **GREEN** (simulated). No remediation required in this cycle.

## Evidence

- `reports/monitoring/drift_report_20260205_022322.json`
