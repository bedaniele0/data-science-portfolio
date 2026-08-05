from pathlib import Path

from src.pipelines.ingest_pipeline import run


def test_ingest_pipeline_writes_outputs():
    report = run(Path("configs/ingestion.yaml"))

    assert report["raw_rows"] > 0
    assert report["normalized_rows"] > 0
    assert Path("data/interim/normalized_articles.csv").exists()
    assert Path("reports/ingestion_report.json").exists()
