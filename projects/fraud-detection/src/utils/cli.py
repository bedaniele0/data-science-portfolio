"""CLI wrappers for stable portfolio demo commands."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import uvicorn


def fraud_api() -> None:
    """Run FastAPI service with sane development defaults."""
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=False)


def fraud_dashboard() -> None:
    """Run Streamlit dashboard from project root."""
    project_root = Path(__file__).resolve().parents[2]
    dashboard_path = project_root / "dashboard" / "fraud_detection_dashboard.py"
    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", str(dashboard_path)],
        check=True,
    )

