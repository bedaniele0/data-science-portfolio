# Runbook Operativo - Prediccion de User Score

Autor: Ing. Daniel Varela Perez
Email: bedaniele0@gmail.com
Tel: +52 55 4189 3428
Fecha: 2026-02-06
Version: 1.0

---

## 1. Servicio
- Nombre: batch_user_score
- Tipo: batch diario
- SLA: < 30 minutos por corrida, disponibilidad 99%

## 2. Dependencias
- Datos: input_user_score_batch (CSV/Parquet diario)
- Infraestructura: Docker + scheduler cloud (cron)
- Repositorio: GitHub (monorepo)
 - Storage: S3 (input/predictions/actuals/monitoring)

## 3. Procedimientos

### Deploy
1. Construir imagen Docker:
   `docker build -t user-score-batch:latest -f deployment/Dockerfile .`
2. Publicar imagen a registry.
3. Actualizar scheduler con nueva version.
4. Validar schema (CI): `python src/validate_schema.py --path data/prod/input.csv --schema configs/schema.yaml --section input`

### Rollback
1. Revertir a imagen anterior (tag estable).
2. Ejecutar corrida de verificacion.

### Retraining
- Frecuencia: mensual o por drift critico.
- Script: `python src/train_model.py`
- Validar metricas en `reports/prod/train_metrics.csv`.

## 4. Monitoreo
- Drift de datos: `python src/monitor_data_drift.py`
- Performance: `python src/monitor_performance.py`
- Umbrales: PSI > 0.25 (critico), R2 < baseline - 0.05

## 5. Contactos
- Owner tecnico: Data Science / ML Engineer
- Owner negocio: Product / Analytics Lead

---

**© 2026 - DVP-MASTER Framework - Ing. Daniel Varela Perez**
