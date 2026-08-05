from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

from src.serving.queries import EventStore

ROOT = Path(__file__).resolve().parents[2]


def _resolve(path: str) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else ROOT / candidate


def run(config_path: Path | str = "configs/serving.yaml") -> dict:
    config_file = _resolve(str(config_path))
    config = yaml.safe_load(config_file.read_text(encoding="utf-8"))
    defaults = config.get("query_defaults", {})
    store = EventStore(
        _resolve(config["input"]["database_path"]),
        max_limit=int(defaults.get("max_limit", 100)),
    )
    default_limit = int(defaults.get("default_limit", 10))
    review_limit = int(defaults.get("review_limit", 25))
    search_limit = int(defaults.get("search_limit", 10))
    smoke_search_text = str(defaults.get("smoke_search_text", "asesinado"))

    health = store.health()
    events = store.list_events(limit=default_limit)
    review_items = store.review_queue(limit=review_limit)
    search_results = store.search_articles(smoke_search_text, limit=search_limit)

    top_event_id = events[0]["event_id"] if events else None
    top_event_articles = store.get_event_articles(top_event_id) if top_event_id else []
    report = {
        "database_path": health["database_path"],
        "table_counts": health["table_counts"],
        "events_returned": len(events),
        "review_queue_returned": len(review_items),
        "search_text": smoke_search_text,
        "search_results_returned": len(search_results),
        "top_event_id": top_event_id,
        "top_event_article_count": len(top_event_articles),
        "contract_checks": {
            "has_events": len(events) > 0,
            "has_review_queue": len(review_items) > 0,
            "search_endpoint_has_results": len(search_results) > 0,
            "top_event_has_articles": len(top_event_articles) > 0,
        },
    }

    failed = [name for name, passed in report["contract_checks"].items() if not passed]
    if failed:
        raise RuntimeError(f"Serving contract checks failed: {failed}")

    report_path = _resolve(config["output"]["report_path"])
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate serving query contract against the master database.")
    parser.add_argument("--config", default="configs/serving.yaml")
    args = parser.parse_args()
    report = run(args.config)
    print(report)


if __name__ == "__main__":
    main()
