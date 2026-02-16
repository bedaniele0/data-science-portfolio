"""
Unit tests for helper utilities in train_demand.py

Autor: Ing. Daniel Varela Perez
Email: bedaniele0@gmail.com
Fecha: December 13, 2024
"""

import numpy as np
import yaml

from src.models.train_demand import (
    calculate_forecast_metrics,
    load_config,
    to_python,
)


def test_calculate_forecast_metrics_basic():
    y_true = np.array([1.0, 2.0, 3.0, 4.0])
    y_pred = np.array([1.1, 1.9, 2.8, 4.2])

    metrics = calculate_forecast_metrics(y_true, y_pred)
    for key in ["mae", "rmse", "mape", "bias"]:
        assert key in metrics
        assert metrics[key] >= 0


def test_to_python_converts_numpy_types():
    assert isinstance(to_python(np.float64(1.2)), float)
    assert isinstance(to_python(np.int64(3)), int)
    assert to_python(np.array([1, 2])).__class__ == list
    assert to_python({"a": np.float32(1.5)}) == {"a": 1.5}


def test_load_config_reads_yaml(tmp_path):
    cfg_path = tmp_path / "config.yaml"
    cfg_content = {"model": {"random_state": 42}}
    cfg_path.write_text(yaml.dump(cfg_content))

    cfg = load_config(str(cfg_path))
    assert cfg["model"]["random_state"] == 42
