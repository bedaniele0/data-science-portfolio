# Memory and Context Policy

This project uses repository documents and experiment tracking as the first
layers of persistent memory.

## Sources of durable context

1. `AGENTS.md` for agent operating rules.
2. `README.md` for onboarding and core commands.
3. `docs/decision-log.md` and `docs/adr/` for durable decisions.
4. `specs/` for approved requirements, plans, and tasks.
5. `configs/` for reproducible experiment and serving settings.
6. MLflow/ZenML for experiment runs and artifacts.
7. Git history for implementation evidence.

## What to save

Save durable context when it changes:

- problem framing, target, metric, split, or baseline
- feature policy, leakage assumptions, or exclusion rules
- data source, schema, retention, or privacy constraints
- model family or evaluation strategy
- serving, monitoring, retraining, or drift policy
- dependency and toolchain policy
- recurring failure modes and fixes

## What not to save

Do not persist:

- temporary notebook observations without validation
- raw secrets, tokens, credentials, or private keys
- large command outputs or metric dumps
- unverified hypotheses
- stale dataset snapshots without provenance

## Context hygiene

- Prefer short, specific entries over broad essays.
- Keep each ADR focused on one decision.
- Store metrics in MLflow/ZenML and summarize durable conclusions in ADRs.
- Update or supersede old decisions instead of silently contradicting them.
- Use connected tools or MCP for live external state instead of copying stale snapshots.

## Escalating to external memory

Native Codex memory, `AGENTS.md`, ADRs, specs, Git, and MLflow/ZenML are enough by default.

Consider Engram or another MCP memory layer only when at least two are true:

- multiple repos need shared modeling or architecture memory
- decisions repeatedly get lost across sessions
- several AI tools need the same memory
- there is a need for searchable cross-project timelines
- repo docs and experiment tracking are no longer enough without becoming noisy

If external memory is introduced, keep repo ADRs and experiment tracking as the
source of durable project truth.
