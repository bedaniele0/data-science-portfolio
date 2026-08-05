# Deployment

This project has two deployable local services:

- FastAPI service for the serving contract.
- Streamlit dashboard for portfolio review.

## Local commands

```zsh
make validate
make api
make dashboard
```

## Docker

Build both images:

```zsh
docker build --target api -t news-event-observatory-api:local .
docker build --target dashboard -t news-event-observatory-dashboard:local .
```

Run with Docker Compose:

```zsh
docker compose up --build
```

Services:

- API: `http://127.0.0.1:8000/health`
- Dashboard: `http://127.0.0.1:8501`

## CI/CD

GitHub Actions runs:

- `ruff check src tests scripts`
- `make validate`
- Docker build for API and dashboard targets
- `docker compose config`

In this portfolio repository, the active workflow is `.github/workflows/news-event-observatory.yml` at the repository root. If this project is extracted into its own repository, keep the same validation contract in `.github/workflows/ci.yml`.

The project should not merge changes unless `make validate` is green locally and in CI.

Docker Compose publishes ports on `127.0.0.1` only. This keeps local demos reachable from the developer machine without exposing them to the wider network.
