from __future__ import annotations

import json
from pathlib import Path

REQUIRED_FILES = [
    "configs/ingestion.yaml",
    "configs/relevance.yaml",
    "configs/relevance_rules.yaml",
    "configs/clustering.yaml",
    "configs/storage.yaml",
    "configs/serving.yaml",
    "configs/dashboard.yaml",
    "LICENSE",
    "docs/privacy-review.md",
    "docs/assets/architecture.svg",
    "docs/assets/dashboard-preview.svg",
    "Dockerfile",
    "docker-compose.yml",
    ".dockerignore",
    "docs/deployment.md",
    "data/raw/demo/google_news_sample_2026-02-16_2026-02-17.csv",
    "data/interim/normalized_articles.csv",
    "data/processed/scored_articles.csv",
    "data/processed/relevant_articles.csv",
    "data/processed/events.csv",
    "data/processed/article_event_links.csv",
    "data/processed/cluster_review.csv",
    "data/processed/events.db",
    "reports/ingestion_report.json",
    "reports/relevance_report.json",
    "reports/clustering_report.json",
    "reports/master_build_report.json",
    "reports/serving_contract_report.json",
    "reports/dashboard_contract_report.json",
    "notebooks/00_project_overview.ipynb",
    "notebooks/01_ingestion_eda.ipynb",
    "notebooks/02_relevance_baseline_review.ipynb",
    "notebooks/03_event_clustering_review.ipynb",
    "notebooks/04_master_database_review.ipynb",
    "notebooks/05_serving_contract_review.ipynb",
    "notebooks/06_dashboard_contract_review.ipynb",
]

README_REQUIRED_CONTENT = [
    "## Que Veras En El Dashboard",
    "## Comandos Makefile",
    "## Ejecutar Con Docker",
    "## Probar El Proyecto",
    "## Ejecutar El Proyecto",
    "## Validacion Automatica",
    "## CI/CD",
    "uv sync --extra validation --extra dashboard",
    "make help",
    "make validate",
    "make test",
    "make validate-artifacts",
    "make validate-notebooks",
    "make api",
    "make dashboard",
    "docker compose up --build",
    "http://127.0.0.1:8000/health",
    "http://127.0.0.1:8000/docs",
    "http://127.0.0.1:8501",
    "uv run ruff check src tests scripts",
    "dashboard data reconciliation",
]

REPORT_EXPECTATIONS = {
    "reports/ingestion_report.json": ["raw_rows", "normalized_rows", "columns"],
    "reports/relevance_report.json": ["total_articles", "relevant_articles", "relevance_rate"],
    "reports/clustering_report.json": ["total_articles_clustered", "total_events", "needs_review_events"],
    "reports/master_build_report.json": ["database_path", "run_id", "table_counts"],
    "reports/serving_contract_report.json": ["database_path", "table_counts", "contract_checks"],
    "reports/dashboard_contract_report.json": ["database_path", "table_counts", "displayed_kpis", "dashboard_checks"],
}

CI_WORKFLOW_CANDIDATES = [
    ".github/workflows/ci.yml",
    ".github/workflows/news-event-observatory.yml",
]


def _workflow_exists(root: Path) -> bool:
    search_roots = [root, *root.parents]
    return any((base / candidate).exists() for base in search_roots for candidate in CI_WORKFLOW_CANDIDATES)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    missing = [artifact for artifact in REQUIRED_FILES if not (root / artifact).exists()]
    if missing:
        missing_lines = "\n".join(f"- {artifact}" for artifact in missing)
        raise SystemExit(f"Missing required artifacts:\n{missing_lines}")

    if not _workflow_exists(root):
        candidates = "\n".join(f"- {candidate}" for candidate in CI_WORKFLOW_CANDIDATES)
        raise SystemExit(f"Missing CI workflow. Expected one of:\n{candidates}")

    readme = (root / "README.md").read_text(encoding="utf-8")
    missing_readme_content = [item for item in README_REQUIRED_CONTENT if item not in readme]
    if missing_readme_content:
        missing_lines = "\n".join(f"- {item}" for item in missing_readme_content)
        raise SystemExit(f"README is missing required execution guidance:\n{missing_lines}")

    for report_path, keys in REPORT_EXPECTATIONS.items():
        path = root / report_path
        payload = json.loads(path.read_text())
        missing_keys = [key for key in keys if key not in payload]
        if missing_keys:
            raise SystemExit(f"Report {report_path} is missing keys: {missing_keys}")

    print("Artifact validation passed.")


if __name__ == "__main__":
    main()
