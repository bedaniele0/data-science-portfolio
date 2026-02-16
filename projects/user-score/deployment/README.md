# Deployment (Batch)

## Cron ejemplo

```
0 2 * * * docker run --rm -v /data:/app/data user-score-batch:latest
```

## Flujo diario
1. Cargar snapshot diario en S3 (`.../input/dt=YYYY-MM-DD/input.csv`)
2. Ejecutar batch (Docker o scheduler cloud)
3. Escribir predicciones en S3 (`.../predictions/dt=YYYY-MM-DD/predictions.csv`)
4. Cargar labels reales en S3 (`.../actuals/dt=YYYY-MM-DD/actuals.csv`)
5. Ejecutar monitoreo y guardar outputs en S3 (`.../monitoring/dt=YYYY-MM-DD/`)
