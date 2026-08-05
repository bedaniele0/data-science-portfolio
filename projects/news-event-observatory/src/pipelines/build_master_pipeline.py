from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

from src.storage.database import get_engine, table_counts
from src.storage.repositories import TABLE_ORDER, load_csv_to_table, write_pipeline_run

ROOT = Path(__file__).resolve().parents[2]


def _resolve(path: str) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else ROOT / candidate


def run(config_path: Path | str = "configs/storage.yaml") -> dict:
    config_file = _resolve(str(config_path))
    config = yaml.safe_load(config_file.read_text())
    input_cfg = config["input"]
    output_cfg = config["output"]
    load_cfg = config.get("load", {})

    database_path = _resolve(output_cfg["database_path"])
    engine = get_engine(database_path)
    if_exists = str(load_cfg.get("if_exists", "replace"))

    source_tables = {
        "articles": _resolve(input_cfg["normalized_articles_path"]),
        "scored_articles": _resolve(input_cfg["scored_articles_path"]),
        "events": _resolve(input_cfg["events_path"]),
        "article_event_links": _resolve(input_cfg["article_event_links_path"]),
        "review_queue": _resolve(input_cfg["review_queue_path"]),
    }

    loaded_counts = {}
    for table_name, csv_path in source_tables.items():
        loaded_counts[table_name] = load_csv_to_table(csv_path, table_name, engine, if_exists=if_exists)

    run_id = write_pipeline_run(
        engine,
        source=str(load_cfg.get("pipeline_run_source", "local")),
        counts=loaded_counts,
        if_exists=if_exists,
    )
    counts = table_counts(engine, TABLE_ORDER)
    report = {
        "database_path": str(database_path),
        "run_id": run_id,
        "table_counts": counts,
        "loaded_counts": loaded_counts,
    }

    report_path = _resolve(output_cfg["report_path"])
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Build master SQLite database from processed artifacts.")
    parser.add_argument("--config", default="configs/storage.yaml")
    args = parser.parse_args()
    report = run(args.config)
    print(report)


if __name__ == "__main__":
    main()
