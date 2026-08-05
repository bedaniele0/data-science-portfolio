from __future__ import annotations

import pandas as pd

from src.dashboard.view_model import build_dashboard_snapshot, frame, kpi_summary


def test_frame_returns_dataframe() -> None:
    result = frame([{"event_id": "evt_1", "article_count": 2}])
    assert isinstance(result, pd.DataFrame)
    assert result.iloc[0]["event_id"] == "evt_1"


def test_kpi_summary_uses_zero_defaults() -> None:
    snapshot = {"table_counts": {"articles": 10, "events": 2}}
    assert kpi_summary(snapshot) == {
        "articles": 10,
        "scored_articles": 0,
        "events": 2,
        "review_queue": 0,
    }


def test_dashboard_snapshot_reconciles_displayed_kpis_with_processed_tables() -> None:
    snapshot = build_dashboard_snapshot("configs/dashboard.yaml")

    assert snapshot["displayed_kpis"] == {
        "articles": snapshot["table_counts"]["articles"],
        "scored_articles": snapshot["table_counts"]["scored_articles"],
        "events": snapshot["table_counts"]["events"],
        "review_queue": snapshot["table_counts"]["review_queue"],
    }
    assert snapshot["dashboard_checks"]["kpi_articles_matches_table_count"]
    assert snapshot["dashboard_checks"]["kpi_scored_articles_matches_table_count"]
    assert snapshot["dashboard_checks"]["kpi_events_matches_table_count"]
    assert snapshot["dashboard_checks"]["kpi_review_queue_matches_table_count"]
