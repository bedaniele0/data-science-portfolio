# Data

This project keeps a small raw seed sample for reproducibility:

- `data/raw/demo/google_news_sample_2026-02-16_2026-02-17.csv`

Generated data is intentionally not tracked by Git:

- `data/interim/`
- `data/processed/`

Run `make validate` to regenerate all processed artifacts, reports and the SQLite database.

Publication note: the seed sample contains public news metadata and URLs. Review `docs/privacy-review.md` before publishing the repository.
