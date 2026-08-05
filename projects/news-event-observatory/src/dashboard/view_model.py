from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
import yaml

from src.serving.queries import EventStore

ROOT = Path(__file__).resolve().parents[2]


def resolve_path(path: str | Path) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else ROOT / candidate


def load_dashboard_config(config_path: Path | str = "configs/dashboard.yaml") -> dict[str, Any]:
    config_file = resolve_path(config_path)
    return yaml.safe_load(config_file.read_text(encoding="utf-8"))


def create_store(config: dict[str, Any]) -> EventStore:
    dashboard_cfg = config.get("dashboard", {})
    return EventStore(
        resolve_path(config["input"]["database_path"]),
        max_limit=int(dashboard_cfg.get("default_event_limit", 100)),
    )


def build_dashboard_snapshot(config_path: Path | str = "configs/dashboard.yaml") -> dict[str, Any]:
    config = load_dashboard_config(config_path)
    dashboard_cfg = config.get("dashboard", {})
    store = create_store(config)
    event_limit = int(dashboard_cfg.get("default_event_limit", 50))
    review_limit = int(dashboard_cfg.get("default_review_limit", 25))
    media_limit = int(dashboard_cfg.get("default_media_limit", 10))
    search_limit = int(dashboard_cfg.get("search_limit", 20))
    smoke_search_text = str(dashboard_cfg.get("smoke_search_text", "asesinado"))

    events = store.list_events(limit=event_limit)
    top_event_id = events[0]["event_id"] if events else None
    top_event_articles = store.get_event_articles(top_event_id) if top_event_id else []
    review_items = store.review_queue(limit=review_limit)
    search_results = store.search_articles(smoke_search_text, limit=search_limit)
    counts = store.table_counts()
    status_summary = store.event_status_summary()
    media_coverage = store.media_coverage(limit=media_limit)
    displayed_kpis = kpi_summary({"table_counts": counts})

    return {
        "table_counts": counts,
        "displayed_kpis": displayed_kpis,
        "events": events,
        "review_queue": review_items,
        "status_summary": status_summary,
        "media_coverage": media_coverage,
        "search_text": smoke_search_text,
        "search_results": search_results,
        "top_event_id": top_event_id,
        "top_event_articles": top_event_articles,
        "dashboard_checks": {
            "has_events": len(events) > 0,
            "has_status_summary": len(status_summary) > 0,
            "has_media_coverage": len(media_coverage) > 0,
            "has_review_queue": len(review_items) > 0,
            "top_event_has_articles": len(top_event_articles) > 0,
            "kpi_articles_matches_table_count": displayed_kpis["articles"] == int(counts.get("articles", 0)),
            "kpi_scored_articles_matches_table_count": displayed_kpis["scored_articles"]
            == int(counts.get("scored_articles", 0)),
            "kpi_events_matches_table_count": displayed_kpis["events"] == int(counts.get("events", 0)),
            "kpi_review_queue_matches_table_count": displayed_kpis["review_queue"] == int(counts.get("review_queue", 0)),
        },
    }


def frame(rows: list[dict[str, Any]]) -> pd.DataFrame:
    return pd.DataFrame(rows)


def kpi_summary(snapshot: dict[str, Any]) -> dict[str, int]:
    counts = snapshot["table_counts"]
    return {
        "articles": int(counts.get("articles", 0)),
        "scored_articles": int(counts.get("scored_articles", 0)),
        "events": int(counts.get("events", 0)),
        "review_queue": int(counts.get("review_queue", 0)),
    }
