# Deploy

Operational deployment assets live in this project directory and in the portfolio repository root workflow:

- `Dockerfile`: multi-target image for `api` and `dashboard`.
- `docker-compose.yml`: local two-service stack.
- repository root `.github/workflows/news-event-observatory.yml`: lint, E2E validation, Docker Compose validation, and Docker builds.

See `docs/deployment.md` for commands and expected service URLs.
