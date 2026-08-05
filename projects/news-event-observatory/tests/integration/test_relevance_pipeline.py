from pathlib import Path

from src.pipelines.ingest_pipeline import run as run_ingestion
from src.pipelines.relevance_pipeline import run as run_relevance


def test_relevance_pipeline_writes_outputs():
    run_ingestion(Path("configs/ingestion.yaml"))
    report = run_relevance(Path("configs/relevance.yaml"))

    assert report["total_articles"] > 0
    assert "relevance_rate" in report
    assert Path("data/processed/scored_articles.csv").exists()
    assert Path("data/processed/relevant_articles.csv").exists()
    assert Path("reports/relevance_report.json").exists()
