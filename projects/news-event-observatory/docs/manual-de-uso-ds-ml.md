# Manual De Uso DS / ML

Guia practica para iniciar proyectos de data science y machine learning usando
las plantillas y herramientas disponibles en `~/Developer`.

## 1. Carpeta base

Todo parte de:

```zsh
~/Developer
```

La plantilla principal para data science / ML es:

```zsh
~/Developer/templates/sdd-codex-ml-template
~/Developer/templates/sdd-codex-ds-e2e-template
```

## 2. Crear un proyecto nuevo

```zsh
cd ~/Developer
cp -R ~/Developer/templates/sdd-codex-ds-e2e-template mi-proyecto-ds
cd mi-proyecto-ds
rm -rf .git
git init
code .
```

## 3. Iniciar Codex dentro del proyecto

```zsh
codex
```

Prompt recomendado al arrancar:

```text
Lee primero docs/spec.md, docs/architecture.md y docs/codex-operating-rules.md.

Actua como mi agente de desarrollo para este proyecto de data science / machine learning.

No tomes decisiones fuera del diseno aprobado. No cambies el problema, la variable objetivo, el enfoque del modelo, las features, las metricas, la arquitectura, el serving ni el despliegue sin proponerlo primero y esperar aprobacion.

Primero ayudame a construir o revisar:
1. el problem statement,
2. la spec,
3. el plan,
4. las tasks.

No implementes nada hasta que apruebe el plan.
```

## 4. Flujo recomendado de trabajo

Dentro de Codex:

```text
Define o revisa spec, arquitectura, plan, tasks, implementacion y validacion.
```

Orden de trabajo:

1. Spec
2. Clarify
3. Plan
4. Tasks
5. Implement
6. Verify
7. Commit

## 5. Estructura del proyecto

```text
data/
  raw/
  interim/
  processed/
  external/
notebooks/
src/
  pipelines/
  features/
  models/
  evaluation/
  serving/
tests/
reports/
artifacts/
configs/
scripts/
deploy/
```

Uso sugerido:

- `data/raw/`: datos originales
- `data/interim/`: datos parcialmente limpios
- `data/processed/`: datos listos para modelado
- `notebooks/`: exploracion y demos
- `src/pipelines/`: entrenamiento end-to-end
- `src/evaluation/`: metricas, drift, fairness, PSI
- `src/serving/`: API del modelo
- `reports/`: resultados y reportes
- `artifacts/`: modelos y salidas serializadas

## 6. Entorno de data science

Entorno global ya disponible:

```zsh
~/Developer/.venvs/data-science
```

Helpers en shell:

```zsh
jlabds
zenmlds
mlflowds
mlflowui
```

Uso:

- abrir JupyterLab:
  ```zsh
  jlabds
  ```
- ver version de ZenML:
  ```zsh
  zenmlds version
  ```
- ver version de MLflow:
  ```zsh
  mlflowds --version
  ```
- abrir MLflow UI:
  ```zsh
  mlflowui
  ```

## 7. Notebook maestro

Notebook incluido:

```text
notebooks/01_ml_concepts_master_demo.ipynb
```

Sirve para practicar:

- Accuracy
- Precision
- Recall
- F1
- AUC
- Confusion Matrix
- Threshold
- Cross-validation
- SMOTE
- SHAP
- Fairness
- Drift
- PSI
- A/B testing

## 8. Correr el pipeline base

Con el entorno global:

```zsh
~/Developer/.venvs/data-science/bin/python -m src.pipelines.train_pipeline
```

O con entorno local del proyecto:

```zsh
uv venv .venv
source .venv/bin/activate
uv sync
uv run python -m src.pipelines.train_pipeline
```

Esto entrena un modelo base, registra metricas en MLflow, genera artefactos y
deja el modelo listo para serving.

El pipeline lee `configs/training.yaml`. Ese archivo debe reflejar la decision
aprobada de experimento, modelo, split, threshold, SMOTE y explainability.

## 8.1 Extras opcionales

El entorno base se mantiene ligero. Instala extras segun la necesidad real:

```zsh
uv sync --extra notebooks
uv sync --extra explainability
uv sync --extra advanced
uv sync --extra drift
uv sync --extra mlops
uv sync --all-extras
```

- `notebooks`: JupyterLab local.
- `explainability`: SHAP.
- `advanced`: modelos/librerias pesadas como XGBoost, LightGBM, CatBoost, Streamlit, Polars y PyArrow.
- `drift`: Evidently.
- `mlops`: ZenML server y orquestacion.

Antes de usar datos reales completa `docs/dataset-card.md` y
`docs/model-card.md`.

## 9. Abrir MLflow

```zsh
mlflowui
```

Normalmente en:

```text
http://127.0.0.1:5000
```

## 10. Levantar API del modelo

Dentro del proyecto:

```zsh
uvicorn src.serving.api:app --reload
```

Normalmente en:

```text
http://127.0.0.1:8000
```

Endpoints base:

- `/health`
- `/predict`

## 11. Medir latencia y throughput

Con la API arriba:

```zsh
python scripts/benchmark_api.py
```

Eso reporta:

- requests
- concurrency
- average latency
- p95 latency
- throughput

## 12. Conceptos cubiertos con este stack

Ya puedes practicar directamente:

- Accuracy
- Precision
- Recall
- F1 Score
- AUC / AUC-ROC
- Confusion Matrix
- Overfitting
- Underfitting
- Threshold
- Cross-validation
- Random Forest
- XGBoost
- SMOTE
- Brier Score
- KS Statistic
- Drift
- PSI
- Feature Engineering
- Regularizacion L1/L2
- A/B Testing
- Fairness
- SHAP
- Model Registry
- CI/CD a nivel de repo
- API
- Latency
- Throughput
- ROI

## 13. Regla clave para trabajar con Codex

Siempre deja claro:

```text
No cambies el problema, target, features, metrica, modelo, fairness policy,
drift policy, API o deployment sin aprobacion.
Primero revisa constitucion, spec, plan y tasks.
Luego implementa.
```

## 14. Procedimiento corto por proyecto

1. Crear proyecto desde plantilla
2. Abrir VS Code
3. Iniciar Codex
4. Crear spec
5. Aclarar ambiguedades
6. Crear plan
7. Crear tasks
8. Implementar pipeline
9. Validar metricas
10. Revisar fairness / drift / explainability
11. Registrar en MLflow
12. Exponer API
13. Medir latencia / throughput
14. Commit

## 15. Comandos resumidos

Crear proyecto:

```zsh
cd ~/Developer
cp -R ~/Developer/templates/sdd-codex-ml-template mi-proyecto-ds
cd mi-proyecto-ds
rm -rf .git
git init
code .
codex
```

Jupyter:

```zsh
jlabds
```

Pipeline:

```zsh
uv run python -m src.pipelines.train_pipeline
```

MLflow:

```zsh
mlflowui
```

API:

```zsh
uvicorn src.serving.api:app --reload
```

Benchmark:

```zsh
python scripts/benchmark_api.py
```
