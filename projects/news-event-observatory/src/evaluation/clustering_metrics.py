from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


def build_clustering_report(events: pd.DataFrame, links: pd.DataFrame, *, source_path: str, labels_path: str | None = None) -> dict[str, Any]:
    total_events = len(events)
    total_articles = len(links)
    singleton_events = int((events["article_count"] == 1).sum()) if not events.empty else 0
    needs_review = int((events["status"] == "needs_review").sum()) if not events.empty else 0
    return {
        "source_path": source_path,
        "labels_path": labels_path or "",
        "total_articles_clustered": total_articles,
        "total_events": total_events,
        "singleton_events": singleton_events,
        "singleton_rate": float(singleton_events / total_events) if total_events else 0.0,
        "needs_review_events": needs_review,
        "needs_review_rate": float(needs_review / total_events) if total_events else 0.0,
        "max_articles_per_event": int(events["article_count"].max()) if not events.empty else 0,
        "mean_articles_per_event": float(events["article_count"].mean()) if not events.empty else 0.0,
        "metrics_available": False,
    }


def write_json(report: dict[str, Any], path: Path | str) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
