# Drift Interpretation Guide

## PSI (Population Stability Index)
- < 0.10: estable
- 0.10–0.25: cambio moderado
- >= 0.25: cambio significativo

## KS Decay
- < 10%: estable
- 10–20%: revisar
- > 20%: degradación crítica

## Recomendaciones
- Validar calidad de datos y cambios en pipeline
- Revisar distribución de features clave (PAY_0, LIMIT_BAL, utilization_1)
- Si drift persiste, reentrenar
