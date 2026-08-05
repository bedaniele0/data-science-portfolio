from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support


def build_relevance_report(scored: pd.DataFrame, *, source_path: str, labels_path: str | None = None) -> dict[str, Any]:
    relevant = scored["is_relevant"].astype(bool)
    report: dict[str, Any] = {
        "source_path": source_path,
        "labels_path": labels_path or "",
        "total_articles": len(scored),
        "relevant_articles": int(relevant.sum()),
        "relevance_rate": float(relevant.mean()) if len(scored) else 0.0,
        "event_term_articles": int(scored["has_event_terms"].astype(bool).sum()),
        "actor_term_articles": int(scored["has_actor_terms"].astype(bool).sum()),
        "top_event_term_groups": _top_matches(scored, "matched_event_terms"),
        "top_actor_term_groups": _top_matches(scored, "matched_actor_terms"),
        "metrics_available": False,
    }
    return report


def add_label_metrics(report: dict[str, Any], scored: pd.DataFrame, labels: pd.DataFrame) -> tuple[dict[str, Any], pd.DataFrame]:
    if "article_id" not in labels.columns or "is_relevant_label" not in labels.columns:
        raise ValueError("Labels must include article_id and is_relevant_label columns.")

    joined = scored.merge(labels[["article_id", "is_relevant_label"]], on="article_id", how="inner")
    if joined.empty:
        report["metrics_available"] = False
        report["metrics_note"] = "No scored rows matched labels."
        return report, pd.DataFrame()

    y_true = joined["is_relevant_label"].astype(bool)
    y_pred = joined["is_relevant"].astype(bool)
    precision, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, average="binary", zero_division=0)
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[False, True]).ravel()

    report.update(
        {
            "metrics_available": True,
            "labeled_rows": len(joined),
            "precision": float(precision),
            "recall": float(recall),
            "f1": float(f1),
            "confusion_matrix": {"tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp)},
        }
    )
    errors = joined.loc[y_true != y_pred].copy()
    return report, errors


def write_json(report: dict[str, Any], path: Path | str) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _top_matches(scored: pd.DataFrame, column: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for value in scored[column].dropna().astype(str):
        for part in [item for item in value.split(";") if item]:
            counts[part] = counts.get(part, 0) + 1
    return dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))
