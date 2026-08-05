from __future__ import annotations

from src.pipelines.build_master_pipeline import run as run_master
from src.pipelines.clustering_pipeline import run as run_clustering
from src.pipelines.dashboard_contract_pipeline import run as run_dashboard_contract
from src.pipelines.ingest_pipeline import run as run_ingest
from src.pipelines.relevance_pipeline import run as run_relevance
from src.pipelines.serving_contract_pipeline import run as run_serving_contract


def test_dashboard_contract_pipeline() -> None:
    run_ingest("configs/ingestion.yaml")
    run_relevance("configs/relevance.yaml")
    run_clustering("configs/clustering.yaml")
    run_master("configs/storage.yaml")
    run_serving_contract("configs/serving.yaml")
    report = run_dashboard_contract("configs/dashboard.yaml")

    assert report["table_counts"]["articles"] == 668
    assert report["table_counts"]["scored_articles"] == 668
    assert report["table_counts"]["events"] == 8
    assert report["table_counts"]["review_queue"] == 8
    assert report["displayed_kpis"] == {
        "articles": 668,
        "scored_articles": 668,
        "events": 8,
        "review_queue": 8,
    }
    assert report["events_returned"] == 8
    assert report["review_queue_returned"] == 8
    assert report["media_coverage_returned"] > 0
    assert all(report["dashboard_checks"].values())
