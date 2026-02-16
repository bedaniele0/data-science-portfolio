"""
monitoring_run.py - Verificación rápida de salud y drift
=======================================================
Ejecuta checks ligeros de modelo/datos y genera un resumen de monitoreo.

Autor: Ing. Daniel Varela Perez
Email: bedaniele0@gmail.com
Tel: +52 55 4189 3428
Metodología: DVP-PRO
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

import joblib
import numpy as np
import pandas as pd


def load_recent_data(path: Path) -> pd.DataFrame:
    return pd.read_parquet(path)


def data_drift_snapshot(df: pd.DataFrame) -> Dict[str, float]:
    # Ligero snapshot: media y std para primeras 5 columnas numéricas
    numeric_cols = [c for c in df.columns if np.issubdtype(df[c].dtype, np.number)]
    summary_cols = numeric_cols[:5]
    stats = {}
    for col in summary_cols:
        stats[col] = {
            "mean": float(df[col].mean()),
            "std": float(df[col].std()),
        }
    return stats


def main() -> None:
    model_path = Path("models/improved_recall_threshold_model.pkl")
    data_path = Path("data/processed/test_clean.parquet")
    report_path = Path("reports/monitoring/healthcheck.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)

    report = {"model_exists": model_path.exists(), "data_exists": data_path.exists()}

    if model_path.exists():
        model = joblib.load(model_path)
        report["model_n_features"] = int(getattr(model, "n_features_in_", 0))

    if data_path.exists():
        df = load_recent_data(data_path)
        report["data_shape"] = [int(df.shape[0]), int(df.shape[1])]
        report["drift_snapshot"] = data_drift_snapshot(df)

    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print("✅ Monitoreo básico ejecutado")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
