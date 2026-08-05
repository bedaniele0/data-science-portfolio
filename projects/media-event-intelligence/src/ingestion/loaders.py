from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.ingestion.schema import REQUIRED_RAW_COLUMNS


def load_csv(path: Path | str) -> pd.DataFrame:
    input_path = Path(path)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    df = pd.read_csv(input_path, dtype=str, keep_default_na=False)
    missing = [col for col in REQUIRED_RAW_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    return df
