# E2E Data Science Validation Ecosystem

This repository is the reference pattern for building validated end-to-end data science projects.

## Goal

Every project should be reproducible from raw or seed data to a usable product surface, with automated gates that catch broken code, missing artifacts, invalid notebooks and deployment drift before publication.

## Required Project Layers

| Layer | Required artifacts | Validation |
| --- | --- | --- |
| Problem framing | `docs/spec.md`, `docs/decision-log.md` | Reviewed before implementation |
| Data contract | `configs/*.yaml`, `src/ingestion`, `data/README.md` | Pipeline run + artifact checks |
| Baseline model | `src/models`, `src/evaluation`, reports | Unit tests + integration tests |
| Storage contract | SQLite or warehouse schema | Build pipeline + table counts |
| Serving contract | query layer/API | Contract report + API tests |
| Product surface | dashboard/app/report | Dashboard contract + data reconciliation + notebook review |
| Documentation | `README.md`, architecture, data/model cards | Artifact validation |
| Deployment | Docker, Compose, CI/CD | Docker build + smoke tests |

## Required Make Targets

Every E2E project should expose these targets or their domain equivalents:

```zsh
make help
make validate
make test
make validate-artifacts
make validate-notebooks
```

Project-specific targets should follow the data flow. For this project:

```zsh
make ingest
make relevance
make clustering
make master
make serving
make dashboard-contract
make api
make dashboard
```

## README Execution Contract

Every E2E data science project must have a friendly README that contains everything needed to execute, validate and inspect the project without reading the source code first.

Required README content:

- project purpose and portfolio value;
- architecture overview;
- setup command;
- full validation command;
- all Makefile targets or equivalent commands;
- test commands;
- notebook validation command;
- artifact validation command;
- local service URLs;
- Docker build and run commands;
- CI/CD summary;
- data/privacy publication notes.

README friendliness rule: run commands, test commands and local URLs must appear near the top of the README, before deep architecture details.

Canonical contract: `docs/readme-execution-contract.md`.

This is enforced by `scripts/validate_artifacts.py`, so `make validate` fails when execution guidance disappears from the README.

## Dashboard Data Reconciliation

Every project with a dashboard must validate that the visible dashboard values match the official processed project outputs.

Minimum contract:

- define the dashboard data source of truth, usually the serving query layer or processed database;
- expose the KPI values used by the dashboard as a testable snapshot, not only as visual widgets;
- compare displayed KPI values against source tables, reports or model artifacts;
- include the reconciliation in the dashboard contract report;
- fail `make validate` when dashboard numbers drift from processed data.

For this project, `reports/dashboard_contract_report.json` must include `displayed_kpis`, `table_counts` and `dashboard_checks`.

## Component Completion Rule

A component is not done until it has:

- production code under `src/`;
- configuration under `configs/` when behavior is tunable;
- at least one focused unit or integration test when risk justifies it;
- generated reports or artifacts when the component produces data;
- a notebook only when it adds review, EDA or portfolio narrative;
- documentation updates for architecture/data/usage;
- green `make validate`.

## Validation Gate

The full gate must run locally and in CI:

```zsh
uv sync --extra validation --extra dashboard
uv run ruff check src tests scripts
make validate
docker compose config
docker build --target api -t media-event-intelligence-api:local .
docker build --target dashboard -t media-event-intelligence-dashboard:local .
```

For deployed projects, add service smoke tests after build.

## Notebook Policy

- Notebooks are review and communication artifacts.
- Pipeline logic belongs in `src/`.
- Every notebook must execute with `pytest --nbmake notebooks`.
- If a notebook fails, the component is not complete.

## Publication Readiness

Before GitHub publication:

- run the privacy review;
- confirm `.gitignore` excludes generated outputs and secrets;
- keep enough seed data to reproduce the demo;
- include README visuals, commands, URLs and validation status;
- run the full validation gate one final time.
