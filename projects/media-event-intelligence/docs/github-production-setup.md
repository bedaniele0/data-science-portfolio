# GitHub Production Setup

Use this after the project has a GitHub remote.

## CI/CD Mode

In this portfolio repository, CI/CD is handled by the root workflow:

```text
.github/workflows/media-event-intelligence.yml
```

The workflow runs lint, `make validate`, `docker compose config`, and Docker image builds for API and dashboard.

If this project is extracted into a standalone repository, keep the same validation contract in `.github/workflows/ci.yml`.

## Release Please

Requirements:

- Use Conventional Commits: `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`.
- Add Release Please only if the project is published as a standalone package or versioned demo.
- For ML projects, update release notes with model/data caveats when needed.

## CodeQL

CodeQL Python scanning can be added as a portfolio-level or standalone workflow when the repository policy requires it.

Private repositories may require GitHub Advanced Security depending on the plan.

## Branch Protection

After pushing the repo to GitHub, protect `main`.

Recommended settings:

- Require pull request before merging.
- Require status checks to pass.
- Require branches to be up to date before merging.
- Require conversation resolution before merging.
- Restrict force pushes.
- Restrict deletions.
- Include administrators only when the project is production critical.

Recommended required checks:

- `Media Event Intelligence E2E / validate`

For ML projects, do not require release automation until the model or package is
actually versioned for external use.
