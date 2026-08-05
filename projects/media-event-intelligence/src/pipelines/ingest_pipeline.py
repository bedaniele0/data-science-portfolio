from __future__ import annotations

import argparse
from pathlib import Path

import yaml

from src.ingestion.loaders import load_csv
from src.ingestion.normalize import normalize_articles
from src.ingestion.reporting import build_ingestion_report, write_report

ROOT = Path(__file__).resolve().parents[2]


def _resolve(path: str) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else ROOT / candidate


def run(config_path: Path | str) -> dict:
    config_file = _resolve(str(config_path))
    config = yaml.safe_load(config_file.read_text())

    input_cfg = config["input"]
    output_cfg = config["output"]
    quality_cfg = config.get("quality", {})

    if input_cfg.get("type") != "csv":
        raise ValueError("Only CSV ingestion is implemented in component 1.")

    raw = load_csv(_resolve(input_cfg["path"]))
    normalized = normalize_articles(
        raw,
        source_name=input_cfg.get("source_name", "unknown"),
        drop_placeholder_rows=bool(quality_cfg.get("drop_placeholder_rows", True)),
        drop_empty_title=bool(quality_cfg.get("drop_empty_title", True)),
        deduplicate_by=tuple(quality_cfg.get("deduplicate_by", ["url", "title", "media"])),
    )

    output_path = _resolve(output_cfg["normalized_articles_path"])
    output_path.parent.mkdir(parents=True, exist_ok=True)
    normalized.to_csv(output_path, index=False)

    report = build_ingestion_report(raw, normalized, source_name=input_cfg.get("source_name", "unknown"))
    write_report(report, _resolve(output_cfg["report_path"]))
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Run article ingestion pipeline.")
    parser.add_argument("--config", default="configs/ingestion.yaml")
    args = parser.parse_args()
    report = run(args.config)
    print(report)


if __name__ == "__main__":
    main()
