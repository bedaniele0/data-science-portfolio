from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.dashboard.view_model import build_dashboard_snapshot, load_dashboard_config, resolve_path


def run(config_path: Path | str = "configs/dashboard.yaml") -> dict:
    config = load_dashboard_config(config_path)
    snapshot = build_dashboard_snapshot(config_path)
    report = {
        "database_path": str(resolve_path(config["input"]["database_path"])),
        "table_counts": snapshot["table_counts"],
        "displayed_kpis": snapshot["displayed_kpis"],
        "events_returned": len(snapshot["events"]),
        "review_queue_returned": len(snapshot["review_queue"]),
        "media_coverage_returned": len(snapshot["media_coverage"]),
        "search_text": snapshot["search_text"],
        "search_results_returned": len(snapshot["search_results"]),
        "top_event_id": snapshot["top_event_id"],
        "top_event_article_count": len(snapshot["top_event_articles"]),
        "dashboard_checks": snapshot["dashboard_checks"],
    }
    failed = [name for name, passed in report["dashboard_checks"].items() if not passed]
    if failed:
        raise RuntimeError(f"Dashboard contract checks failed: {failed}")
    report_path = resolve_path(config["output"]["report_path"])
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate dashboard data contract against the serving query layer.")
    parser.add_argument("--config", default="configs/dashboard.yaml")
    args = parser.parse_args()
    report = run(args.config)
    print(report)


if __name__ == "__main__":
    main()
