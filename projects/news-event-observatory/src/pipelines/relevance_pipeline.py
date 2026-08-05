from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
import yaml

from src.evaluation.relevance_metrics import add_label_metrics, build_relevance_report, write_json
from src.models.relevance_rules import RelevanceRules, apply_relevance_rules

ROOT = Path(__file__).resolve().parents[2]


def _resolve(path: str) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else ROOT / candidate


def run(config_path: Path | str = "configs/relevance.yaml") -> dict:
    config_file = _resolve(str(config_path))
    config = yaml.safe_load(config_file.read_text())
    input_cfg = config["input"]
    output_cfg = config["output"]
    quality_cfg = config.get("quality", {})

    articles_path = _resolve(input_cfg["articles_path"])
    rules_path = _resolve(input_cfg["rules_path"])
    labels_path = _resolve(input_cfg.get("labels_path", "")) if input_cfg.get("labels_path") else None

    articles = pd.read_csv(articles_path, dtype=str, keep_default_na=False)
    rules = RelevanceRules.from_yaml(rules_path)
    scored = apply_relevance_rules(
        articles,
        rules,
        text_fields=tuple(quality_cfg.get("text_fields", ["title", "description"])),
    )

    scored_path = _resolve(output_cfg["scored_articles_path"])
    relevant_path = _resolve(output_cfg["relevant_articles_path"])
    scored_path.parent.mkdir(parents=True, exist_ok=True)
    relevant_path.parent.mkdir(parents=True, exist_ok=True)
    scored.to_csv(scored_path, index=False)
    scored.loc[scored["is_relevant"].astype(bool)].to_csv(relevant_path, index=False)

    report = build_relevance_report(scored, source_path=str(articles_path), labels_path=str(labels_path) if labels_path else None)
    errors = pd.DataFrame()
    if labels_path and labels_path.exists():
        labels = pd.read_csv(labels_path)
        report, errors = add_label_metrics(report, scored, labels)
    elif quality_cfg.get("require_labels_for_metrics", False):
        raise FileNotFoundError(f"Labels file not found: {labels_path}")

    write_json(report, _resolve(output_cfg["report_path"]))
    errors_path = _resolve(output_cfg["errors_path"])
    errors_path.parent.mkdir(parents=True, exist_ok=True)
    errors.to_csv(errors_path, index=False)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Run relevance filtering pipeline.")
    parser.add_argument("--config", default="configs/relevance.yaml")
    args = parser.parse_args()
    report = run(args.config)
    print(report)


if __name__ == "__main__":
    main()
