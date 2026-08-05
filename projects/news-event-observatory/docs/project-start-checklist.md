# ML Project Start Checklist

## Problem

- What business or research problem are we solving?
- What exact decision will the model support?
- What is the target variable?
- What does success look like?

## Data

- Where does the data come from?
- Is there label leakage risk?
- Are there privacy or compliance concerns?
- What split strategy is valid for this problem?
- What schema, grain, time window, and data quality checks are required?
- Is `docs/dataset-card.md` complete enough for source, schema, split, privacy and retention?

## Modeling

- What is the baseline model?
- What is the primary metric?
- What secondary metrics matter?
- Is explainability required?
- What model families, features, or transformations are explicitly out of scope?
- Is `docs/model-card.md` complete enough for intended use, metrics, risks and serving?
- Is `configs/training.yaml` aligned with the approved experiment, model, split and threshold?

## Production

- How will the model be served?
- What artifact format is expected?
- How will retraining happen?
- What monitoring or drift checks are needed?
- What latency and throughput targets must the API meet?
- What business metric or ROI definition matters after deployment?

## README Execution

- Does `README.md` explain the project purpose and portfolio value?
- Does it include setup instructions from a clean environment?
- Does it list every `make` target or task runner command needed to operate the project?
- Does it include `make validate`, test commands, notebook validation and artifact validation?
- Does it include local URLs for API, dashboard, notebooks or app surfaces?
- Does it include Docker commands when Docker exists?
- Does it summarize CI/CD and publication/privacy notes?
- Does `scripts/validate_artifacts.py` enforce the README execution contract?

## GitHub Readiness

- Does the repo have a GitHub remote?
- Are Conventional Commits required?
- Should Release Please be active for this model/package?
- Should CodeQL be required in branch protection?
- What exact CI check names must protect `main`?

## AI Workflow

- Has Codex completed an Explorer pass over data, notebooks, code and configs?
- Is the approved target, metric, split and baseline documented?
- Are feature policy, leakage risks, privacy and retention constraints explicit?
- What live sources require connectors or MCP instead of assumptions?
- What configs/docs/specs must be updated if implementation changes the approved intent?

## Persistent Memory

- Does this project need an ADR for the current modeling or architecture decision?
- Has `docs/decision-log.md` been updated?
- Are durable metrics/artifacts tracked in MLflow or ZenML?
- Is the decision durable enough for repo docs, or temporary enough for chat/PR only?
- Is external memory/MCP justified, or are repo docs plus experiment tracking enough?

## Agent boundaries

- Codex must stay inside the approved problem framing and plan.
- Codex must ask before changing model family, metric, data split, features, or deployment design.
