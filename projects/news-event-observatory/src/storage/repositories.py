from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

import pandas as pd
from sqlalchemy import Engine

TABLE_ORDER = [
    "articles",
    "scored_articles",
    "events",
    "article_event_links",
    "review_queue",
    "pipeline_runs",
]


def load_csv_to_table(path: Path | str, table_name: str, engine: Engine, *, if_exists: str = "replace") -> int:
    csv_path = Path(path)
    if not csv_path.exists():
        raise FileNotFoundError(f"Required CSV does not exist: {csv_path}")
    df = pd.read_csv(csv_path, dtype=str, keep_default_na=False)
    df = _coerce_table_types(df, table_name)
    df.to_sql(table_name, engine, if_exists=if_exists, index=False)
    return len(df)


def write_pipeline_run(engine: Engine, *, source: str, counts: dict[str, int], if_exists: str = "replace") -> str:
    run_id = str(uuid4())
    row = pd.DataFrame(
        [
            {
                "run_id": run_id,
                "run_started_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
                "source": source,
                "articles_rows": counts.get("articles", 0),
                "scored_articles_rows": counts.get("scored_articles", 0),
                "events_rows": counts.get("events", 0),
                "article_event_links_rows": counts.get("article_event_links", 0),
                "review_queue_rows": counts.get("review_queue", 0),
            }
        ]
    )
    row.to_sql("pipeline_runs", engine, if_exists=if_exists, index=False)
    return run_id


def _coerce_table_types(df: pd.DataFrame, table_name: str) -> pd.DataFrame:
    result = df.copy()
    if table_name == "scored_articles":
        for column in ["is_relevant", "has_event_terms", "has_actor_terms"]:
            if column in result.columns:
                result[column] = result[column].astype(str).str.lower().isin(["true", "1", "yes"])
        if "relevance_score" in result.columns:
            result["relevance_score"] = pd.to_numeric(result["relevance_score"], errors="coerce").fillna(0.0)
    if table_name == "events":
        for column in ["event_number", "article_count", "media_count", "query_count"]:
            if column in result.columns:
                result[column] = pd.to_numeric(result[column], errors="coerce").fillna(0).astype(int)
        if "confidence" in result.columns:
            result["confidence"] = pd.to_numeric(result["confidence"], errors="coerce").fillna(0.0)
    if table_name == "article_event_links" and "link_confidence" in result.columns:
        result["link_confidence"] = pd.to_numeric(result["link_confidence"], errors="coerce").fillna(0.0)
    if table_name == "review_queue":
        for column in ["article_count", "media_count"]:
            if column in result.columns:
                result[column] = pd.to_numeric(result[column], errors="coerce").fillna(0).astype(int)
        for column in ["confidence", "review_threshold"]:
            if column in result.columns:
                result[column] = pd.to_numeric(result[column], errors="coerce").fillna(0.0)
    return result
