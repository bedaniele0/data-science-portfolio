# proyecto_user_score_ds

Proyecto S-Lite para prediccion de `user_score` con enfoque de regresion.

**Estado del proyecto:** AMARILLO (SIMULADO)  
Evidencia: `reports/monitoring_report.md`, `reports/11_final_report.md`.

## Estructura
- `data/`: dataset original y batch simulado
- `notebooks/`: notebooks de EDA, feature engineering y modelado
- `reports/`: reportes DVP-MASTER y artefactos
- `models/`: artefactos de modelo (demo)
- `src/`: pipeline batch, entrenamiento y monitoreo
- `tests/`: pruebas básicas
- `configs/`: config y schema
- `deployment/`: ejemplos de despliegue batch
- `Dockerfile`: imagen batch (root)
- `Makefile`: atajos de ejecución local
- `pyproject.toml`: metadata + config pytest
- `deployment/aws_eventbridge_scheduler.json`: ejemplo EventBridge Scheduler (AWS)
- `deployment/aws_ecs_task_def.json`: ejemplo ECS Task Definition (AWS)
- `deployment/gcp_cloud_run_job.yaml`: ejemplo Cloud Run Job (GCP)
- `deployment/gcp_cloud_scheduler.yaml`: ejemplo Cloud Scheduler (GCP)

## Entregables principales
- `reports/01_problem_statement.md`
- `reports/kpi_tree.md`
- `reports/business_case.md`
- `reports/03_eda_report.md`
- `reports/data_quality_report.md`
- `reports/02_model_evaluation.md`
- `reports/11_final_report.md`
- `reports/roi_validation.md`
- `reports/lessons_learned.md`
- `reports/monitoring_report.md` (F8 simulado)
- `reports/09_model_card.md`
- `reports/data_contract.md`
- `reports/12_runbook_operativo.md`

## Produccion (batch) - SIMULADO
1. Entrenar y versionar modelo:
   `STORAGE_MODE=local python src/train_model.py`
2. Ejecutar scoring batch:
   `STORAGE_MODE=local python src/batch_scoring.py`
3. Monitoreo:
   `STORAGE_MODE=local python src/monitor_data_drift.py`
   `STORAGE_MODE=local python src/monitor_performance.py`

## Demo
- Batch training: local (`make train`)
- Batch scoring: local (`make score`)
- Monitoring: local (`make monitor`)

## Quickstart (local)
```bash
make install
make train
make score
make monitor
```

## How to run
- Install:
  - `make install`
- Run:
  - `make train`
  - `make score`
  - `make monitor`

## Scripts clave
- `src/train_model.py`: entrenamiento y versionado del modelo.
- `src/batch_scoring.py`: scoring diario batch.
- `src/monitor_data_drift.py`: PSI por feature.
- `src/monitor_performance.py`: MAE/R2 con labels reales.

## E2E (artefactos de ejemplo)
- `data/prod/input.csv`: snapshot diario (50 filas, incluye OOV en `genres`)
- `data/prod/predictions.csv`: generado por batch
- `data/prod/actuals.csv`: labels reales simulados

## Storage
- Produccion usa rutas S3 en `configs/config.yaml` (diseño, SIMULADO).
- Para ejecucion local usa `STORAGE_MODE=local`.
- Validacion de schema: `configs/schema.yaml` + `src/validate_schema.py` (CI y runtime).

## Deployment Parameters (AWS)
```
AWS_REGION=NO_DEFINIDO
S3_BUCKET=NO_DEFINIDO
ECR_REPO_URI=NO_DEFINIDO
ECS_CLUSTER_NAME=NO_DEFINIDO
TASK_ROLE_ARN=NO_DEFINIDO
EXECUTION_ROLE_ARN=NO_DEFINIDO
SCHEDULE_UTC=02:00
```

## Quick Go-Live (AWS)
1. Reemplaza `NO_DEFINIDO` en `configs/config.yaml` y `deployment/aws_*.json`.
2. Publica imagen en ECR y actualiza `ECR_REPO_URI`.
3. Activa el scheduler (EventBridge) y valida outputs en S3.

## Notebooks
- `notebooks/01_eda.ipynb`
- `notebooks/02_feature_engineering.ipynb`
- `notebooks/03_modeling.ipynb`

## Tests
```bash
python3 -m pytest -q
```

Si trabajas con `.venv`, tambien puedes ejecutar:
```bash
./.venv/bin/python -m pytest -q
```

## Repo structure
- `src/` pipeline batch, entrenamiento y monitoreo
- `configs/` config y schema
- `data/` inputs/outputs batch (demo)
- `reports/` reportes y runbook
- `deployment/` ejemplos de despliegue batch

## Notas
- Se implemento multi-hot controlado para `genres` y se probo GradientBoosting.
- MAE se mantiene en objetivo, R2 sigue por debajo del umbral (ver `reports/02_model_evaluation.md`).
- Siguiente mejora sugerida: ampliar vocabulario de `genres` y probar XGBoost/LightGBM.
