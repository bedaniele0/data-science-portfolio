from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


def build_ingestion_report(raw: pd.DataFrame, normalized: pd.DataFrame, *, source_name: str) -> dict[str, Any]:
    return {
        "source": source_name,
        "raw_rows": len(raw),
        "normalized_rows": len(normalized),
        "dropped_rows": int(len(raw) - len(normalized)),
        "unique_media": int(normalized["media"].nunique()) if not normalized.empty else 0,
        "unique_queries": int(normalized["query"].nunique()) if not normalized.empty else 0,
        "min_published_at": str(normalized["published_at"].replace("", pd.NA).min()) if not normalized.empty else "",
        "max_published_at": str(normalized["published_at"].replace("", pd.NA).max()) if not normalized.empty else "",
        "columns": list(normalized.columns),
    }


def write_report(report: dict[str, Any], path: Path | str) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
