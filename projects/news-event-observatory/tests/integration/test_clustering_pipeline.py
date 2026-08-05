from pathlib import Path

from src.pipelines.clustering_pipeline import run as run_clustering
from src.pipelines.ingest_pipeline import run as run_ingestion
from src.pipelines.relevance_pipeline import run as run_relevance


def test_clustering_pipeline_writes_outputs():
    run_ingestion(Path("configs/ingestion.yaml"))
    run_relevance(Path("configs/relevance.yaml"))
    report = run_clustering(Path("configs/clustering.yaml"))

    assert report["total_articles_clustered"] >= 0
    assert "total_events" in report
    assert Path("data/processed/events.csv").exists()
    assert Path("data/processed/article_event_links.csv").exists()
    assert Path("data/processed/cluster_review.csv").exists()
    assert Path("reports/clustering_report.json").exists()
