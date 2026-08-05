# README Execution Contract

Every end-to-end data science project must include a friendly README that lets a real user, reviewer, recruiter or future maintainer execute the project without reverse-engineering the codebase.

## User-Friendly Principle

The README must be written for the person who is trying to run the project, not for the person who built it.

A good README should:

- start with the fastest manual execution path;
- use direct copy/paste commands;
- explain what each command does in plain language;
- show the exact local URLs to open;
- separate execution, testing, Docker and technical architecture;
- avoid burying important run commands deep in the document;
- avoid assuming the user already knows the repo structure.

## Required Sections

A complete README must include:

- project purpose and portfolio value;
- a top-level "run the project" section;
- setup instructions from a clean checkout;
- dashboard/API execution commands when they exist;
- exact local URLs for APIs, dashboards or apps;
- testing and quality commands;
- Makefile command reference or equivalent task runner reference;
- notebook validation command when notebooks exist;
- artifact validation command;
- Docker build and run commands when Docker exists;
- CI/CD summary when workflows exist;
- data/privacy publication notes;
- license reference.

## Required Command Coverage

At minimum, the README must tell the user how to run:

```zsh
uv sync --extra validation --extra dashboard
make help
make validate
make test
make validate-artifacts
make validate-notebooks
uv run ruff check src tests scripts
```

For this project it must also include:

```zsh
make api
make dashboard
docker compose up --build
```

## Required URL Coverage

If local services exist, the README must list their URLs. For this project:

```text
http://127.0.0.1:8000/health
http://127.0.0.1:8000/docs
http://127.0.0.1:8501
```

## Friendliness Checklist

Before publishing, verify that a user can answer these questions from the README alone:

- How do I install dependencies?
- What command proves the project works?
- How do I open the dashboard?
- What URL should I open?
- How do I open the API docs?
- How do I run tests only?
- How do I run notebooks only?
- How do I run with Docker?
- What should I expect to see?
- Where are privacy/publication notes?

## Enforcement

The README contract is enforced by `scripts/validate_artifacts.py` through `README_REQUIRED_CONTENT`.

`make validate` must fail if README execution guidance is removed or becomes incomplete.

## Future Project Rule

When creating a new E2E data science project from this ecosystem, define the README execution contract during project setup, before adding advanced modeling work. Update the required content whenever the project adds a new runtime surface such as an API, dashboard, CLI, Docker image, notebook flow or cloud deployment.
