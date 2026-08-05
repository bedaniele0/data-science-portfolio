# News Event Observatory - Case Study

## Problem

News monitoring produces a high volume of duplicated and semi-structured articles. The project turns public news metadata into a relational event database that can support review, search, and operational dashboards.

## Solution

I designed an end-to-end data science system with ingestion, normalization, relevance scoring, event clustering, SQLite persistence, FastAPI serving, Streamlit visualization, notebooks, and automated validation contracts.

## Technical Highlights

- Reproducible pipelines controlled by `Makefile` targets.
- Demo seed from public Google News metadata, sanitized before publication.
- Relational event model with `articles`, `scored_articles`, `events`, `article_event_links`, `review_queue`, and `pipeline_runs`.
- API contract validation for `/health`, `/events`, `/articles`, `/review-queue`, and `/summary`.
- Dashboard contract validation that reconciles visible KPIs against processed outputs.
- Notebook execution validation with `nbmake` to prevent broken exploratory artifacts.

## Current Results

| Metric | Value |
|---|---:|
| Normalized articles | 668 |
| Candidate events | 8 |
| Review queue events | 8 |
| Media sources | 197 |
| Validated tests | 21 |
| Validated notebooks | 7 |

## How To Run

The project README includes the full manual execution path. Main commands:

```bash
make bootstrap
make validate
make api
make dashboard
```

## Portfolio Value

This project demonstrates applied ML engineering beyond a notebook: data contracts, reproducible pipelines, documented architecture, serving, dashboard validation, Docker readiness, and CI/CD validation.
