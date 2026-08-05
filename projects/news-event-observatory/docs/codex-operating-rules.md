# Codex Operating Rules For ML Projects

## Source of truth

1. User approval
2. `docs/spec.md`
3. `docs/architecture.md`
4. `docs/decision-log.md`
5. Current implementation plan
6. Existing code and approved design

If these conflict, Codex must stop and ask.

## AI operating model

Daniel is the architect and ML owner. Codex may explore, design, implement and
review, but human approval controls problem framing, target, metric, data split,
feature policy, model family, security and deployment decisions.

Use this role sequence for substantial work:

1. Explorer: inspect repo, data sources, schema, notebooks, configs, pipelines,
   dependencies, metrics, artifacts and risks.
2. Designer: propose problem statement, spec, validation strategy, baseline,
   plan, tradeoffs and acceptance criteria.
3. Implementer: make approved changes in reproducible, testable steps.
4. Reviewer: check leakage, metrics, regressions, reproducibility, docs and artifacts.

For small tasks, Codex can perform all roles in one turn. For broad modeling or
production changes, split the roles across turns or subagents.

## SDD pragmatics for ML

- Spec-first: agree on target, metric, split, baseline and business objective before coding.
- Spec-as-source: spec and plan are the approved source of modeling intent.
- Code-as-artifact: code implements the approved experiment or pipeline and may
  be edited, but meaningful changes must update spec, plan, tasks, configs or docs.
- Runtime evidence matters: metrics, artifacts, data profiles and experiment logs
  must be treated as part of the review, not as decoration.

## Persistent memory

Use repo docs and experiment tracking as durable memory before relying on chat history:

- `AGENTS.md` for operating rules.
- `docs/memory-and-context.md` for memory policy.
- `docs/decision-log.md` and `docs/adr/` for durable decisions.
- `specs/` for approved requirements and plans.
- MLflow/ZenML for experiment runs, metrics and artifacts.

Create or update an ADR when implementation changes problem framing, target,
metric, split, feature policy, model family, evaluation, serving, monitoring,
data retention, security posture or deployment.

## Restrictions

Codex must not independently change:

- problem framing
- target variable
- evaluation metric
- train/validation/test strategy
- feature policy
- model family
- deployment architecture
- data retention rules
- security posture
- experiment tracking policy
- production monitoring policy

If any of those need to change, Codex must propose and wait for approval.

## README execution contract

For E2E data science projects, Codex must keep the README executable. If a change adds or changes setup, Makefile targets, APIs, dashboards, notebooks, Docker, CI/CD or validation commands, Codex must update README guidance and keep `scripts/validate_artifacts.py` aligned.

The project is not portfolio-ready if a reviewer cannot execute it from the README.

## Dashboard reconciliation rule

For any E2E data science project with a dashboard, Codex must add an automated check that compares dashboard-visible KPI/table values against the processed data source of truth. The user should not need to ask for this manually. The check belongs in the dashboard contract, must emit evidence in a report, and must be included in `make validate`.

## Verification policy

Before finalizing ML implementation, Codex should run the smallest meaningful gate:

- Unit tests for deterministic code.
- Data validation or schema checks when data changes.
- Baseline or smoke training when modeling code changes.
- Metric report against the approved split when evaluation changes.
- API smoke test when serving changes.
- MLflow/ZenML artifact check when tracking or pipelines change.

If a gate cannot run, report why and what residual risk remains.

## Expected delivery behavior

Every ML implementation should report:

- files changed
- data assumptions
- metric used
- validation performed
- artifacts produced
- next recommended step
- whether README execution guidance changed or remained valid
