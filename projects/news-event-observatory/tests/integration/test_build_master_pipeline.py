from pathlib import Path

from sqlalchemy import text

from src.pipelines.build_master_pipeline import run as run_master
from src.pipelines.clustering_pipeline import run as run_clustering
from src.pipelines.ingest_pipeline import run as run_ingestion
from src.pipelines.relevance_pipeline import run as run_relevance
from src.storage.database import get_engine


def test_build_master_pipeline_writes_sqlite_tables():
    run_ingestion(Path("configs/ingestion.yaml"))
    run_relevance(Path("configs/relevance.yaml"))
    run_clustering(Path("configs/clustering.yaml"))
    report = run_master(Path("configs/storage.yaml"))

    db_path = Path("data/processed/events.db")
    assert db_path.exists()
    assert report["table_counts"]["articles"] == 668
    assert report["table_counts"]["events"] == 8

    engine = get_engine(db_path)
    with engine.connect() as connection:
        tables = connection.execute(text("SELECT name FROM sqlite_master WHERE type='table'")).scalars().all()
    for table_name in ["articles", "scored_articles", "events", "article_event_links", "review_queue", "pipeline_runs"]:
        assert table_name in tables
