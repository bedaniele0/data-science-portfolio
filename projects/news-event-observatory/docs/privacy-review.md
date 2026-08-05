# Privacy and Publication Review

Date: 2026-08-04

## Publication decision

This repository is prepared for portfolio publication with a small seed dataset.
Generated outputs are reproducible and should not be committed by default.

## Data classification

- Source: small demo seed derived from public Google News metadata.
- Contents: news titles, descriptions, media names, publication dates, minimized search URLs, article URLs and derived IDs.
- Intended use: reproducible portfolio demo for data science and ML engineering.

## Automated scan notes

A keyword scan was run for common secret patterns such as private keys, API keys, passwords and email-like credentials. No real credentials were identified.

The raw demo seed was sanitized before publication: Google News search URLs were reduced to their query term and article URL parameters named `token` were removed. Remaining URL text is retained only to make the demo reproducible.

## Publication guardrails

- Do not commit `.env`, credentials or local virtual environments.
- Do not commit generated `data/interim`, `data/processed` or `reports` outputs.
- Keep only the small raw sample needed to reproduce the portfolio pipeline.
- The public repository must not include the original backup folder or unsanitized scraping outputs.
- Re-run `make validate` before publishing or merging changes.

## Residual caveat

The dataset contains public news headlines that may mention real people and violent events. The project should be presented as an event intelligence engineering demo, not as a verified factual adjudication system.
