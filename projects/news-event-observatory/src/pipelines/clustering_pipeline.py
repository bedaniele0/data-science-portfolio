from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
import yaml

from src.evaluation.clustering_metrics import build_clustering_report, write_json
from src.models.event_clustering import ClusteringConfig, cluster_articles

ROOT = Path(__file__).resolve().parents[2]


def _resolve(path: str) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else ROOT / candidate


def run(config_path: Path | str = "configs/clustering.yaml") -> dict:
    config_file = _resolve(str(config_path))
    config = yaml.safe_load(config_file.read_text())
    input_cfg = config["input"]
    output_cfg = config["output"]
    clustering_cfg = config.get("clustering", {})

    relevant_path = _resolve(input_cfg["relevant_articles_path"])
    labels_path = _resolve(input_cfg.get("labels_path", "")) if input_cfg.get("labels_path") else None
    articles = pd.read_csv(relevant_path, dtype=str, keep_default_na=False)

    model_config = ClusteringConfig(
        similarity_threshold=float(clustering_cfg.get("similarity_threshold", 0.32)),
        review_confidence_threshold=float(clustering_cfg.get("review_confidence_threshold", 0.55)),
        max_days_between_articles=int(clustering_cfg.get("max_days_between_articles", 3)),
        text_fields=tuple(clustering_cfg.get("text_fields", ["title", "description"])),
        date_field=str(clustering_cfg.get("date_field", "published_at")),
        article_id_field=str(clustering_cfg.get("article_id_field", "article_id")),
        min_df=int(clustering_cfg.get("min_df", 1)),
        ngram_range=tuple(clustering_cfg.get("ngram_range", [1, 2])),
    )
    events, links, review_queue = cluster_articles(articles, model_config)

    events_path = _resolve(output_cfg["events_path"])
    links_path = _resolve(output_cfg["article_event_links_path"])
    review_path = _resolve(output_cfg["review_queue_path"])
    for output_path in [events_path, links_path, review_path]:
        output_path.parent.mkdir(parents=True, exist_ok=True)

    events.to_csv(events_path, index=False)
    links.to_csv(links_path, index=False)
    review_queue.to_csv(review_path, index=False)

    report = build_clustering_report(
        events,
        links,
        source_path=str(relevant_path),
        labels_path=str(labels_path) if labels_path else None,
    )
    write_json(report, _resolve(output_cfg["report_path"]))
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Run event clustering pipeline.")
    parser.add_argument("--config", default="configs/clustering.yaml")
    args = parser.parse_args()
    report = run(args.config)
    print(report)


if __name__ == "__main__":
    main()
