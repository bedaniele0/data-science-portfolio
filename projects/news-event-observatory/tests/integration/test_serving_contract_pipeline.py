from __future__ import annotations

from src.pipelines.build_master_pipeline import run as run_master
from src.pipelines.clustering_pipeline import run as run_clustering
from src.pipelines.ingest_pipeline import run as run_ingest
from src.pipelines.relevance_pipeline import run as run_relevance
from src.pipelines.serving_contract_pipeline import run as run_serving_contract


def test_serving_contract_pipeline() -> None:
    run_ingest("configs/ingestion.yaml")
    run_relevance("configs/relevance.yaml")
    run_clustering("configs/clustering.yaml")
    run_master("configs/storage.yaml")
    report = run_serving_contract("configs/serving.yaml")

    assert report["table_counts"]["events"] == 8
    assert report["events_returned"] > 0
    assert report["review_queue_returned"] > 0
    assert report["search_results_returned"] > 0
    assert all(report["contract_checks"].values())
