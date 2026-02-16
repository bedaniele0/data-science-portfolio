"""
Unit tests for the main training pipeline in src/models/train_demand.py

Author: Ing. Daniel Varela Perez
Email: bedaniele0@gmail.com
Date: December 15, 2025
"""

import pytest
import yaml
import numpy as np
import pandas as pd
from pathlib import Path

from src.models.train_demand import (
    load_config,
    to_python,
    calculate_forecast_metrics,
    prepare_features_target
)


@pytest.fixture
def temp_config_file(tmp_path: Path) -> str:
    """Fixture to create a temporary YAML config file."""
    config_data = {
        "paths": {"processed_data": "data/processed"},
        "model": {"n_estimators": 100, "learning_rate": 0.05}
    }
    config_file = tmp_path / "test_config.yaml"
    with open(config_file, 'w') as f:
        yaml.dump(config_data, f)
    return str(config_file)


class TestLoadConfig:
    """Tests for the load_config function."""

    def test_load_config_success(self, temp_config_file: str):
        """Test that config is loaded correctly from a valid file."""
        config = load_config(temp_config_file)
        assert config["paths"]["processed_data"] == "data/processed"
        assert config["model"]["n_estimators"] == 100

    def test_load_config_file_not_found(self):
        """Test that an empty dict is returned if the file does not exist."""
        # Suppress logging for this test to keep output clean
        config = load_config("non_existent_file.yaml")
        assert config == {}


class TestToPython:
    """Tests for the to_python utility function."""

    def test_converts_numpy_float(self):
        """Test conversion of numpy float types."""
        assert isinstance(to_python(np.float32(1.23)), float)
        assert to_python(np.float64(1.23)) == 1.23

    def test_converts_numpy_int(self):
        """Test conversion of numpy integer types."""
        assert isinstance(to_python(np.int32(123)), int)
        assert to_python(np.int64(123)) == 123

    def test_converts_numpy_array(self):
        """Test conversion of numpy arrays."""
        arr = np.array([1, 2, 3])
        assert to_python(arr) == [1, 2, 3]

    def test_handles_nested_structures(self):
        """Test recursive conversion in nested dicts and lists."""
        nested_obj = {
            "a": np.float32(1.5),
            "b": [np.int64(1), np.int64(2)],
            "c": {"d": np.array([3, 4])}
        }
        converted = to_python(nested_obj)
        assert isinstance(converted["a"], float)
        assert isinstance(converted["b"][0], int)
        assert converted["c"]["d"] == [3, 4]

    def test_returns_native_python_types_as_is(self):
        """Test that native types are not modified."""
        assert to_python(123) == 123
        assert to_python(1.23) == 1.23
        assert to_python("test") == "test"


class TestCalculateForecastMetrics:
    """Tests for the calculate_forecast_metrics function."""

    def test_basic_calculation(self):
        """Test metrics with simple, non-zero inputs."""
        y_true = np.array([10, 20, 30, 40])
        y_pred = np.array([12, 18, 33, 42])
        metrics = calculate_forecast_metrics(y_true, y_pred)
        assert metrics["mae"] == pytest.approx(2.25)
        assert metrics["rmse"] == pytest.approx(2.291, abs=1e-3)
        assert metrics["wmape"] == pytest.approx(9.0)
        assert metrics["forecast_accuracy"] == pytest.approx(0.91)

    def test_with_zeros_in_true_values(self):
        """Test that WMAPE and other metrics handle zeros correctly."""
        y_true = np.array([0, 10, 0, 20])
        y_pred = np.array([1, 10, -1, 22])
        metrics = calculate_forecast_metrics(y_true, y_pred)
        # sum(abs(y_true - y_pred)) = 1 + 0 + 1 + 2 = 4
        # sum(abs(y_true)) = 0 + 10 + 0 + 20 = 30
        # WMAPE = (4 / 30) * 100
        assert metrics["wmape"] == pytest.approx(13.333, abs=1e-3)
        assert metrics["mae"] == 1.0

    def test_perfect_forecast(self):
        """Test metrics when the forecast is perfect."""
        y_true = np.array([15, 25, 35])
        y_pred = np.array([15, 25, 35])
        metrics = calculate_forecast_metrics(y_true, y_pred)
        assert metrics["mae"] == 0.0
        assert metrics["rmse"] == 0.0
        assert metrics["wmape"] == 0.0
        assert metrics["forecast_accuracy"] == 1.0


class TestPrepareFeaturesTarget:
    """Tests for the prepare_features_target function."""

    @pytest.fixture
    def sample_df(self) -> pd.DataFrame:
        """Fixture for a sample DataFrame."""
        return pd.DataFrame({
            "id": ["id_1", "id_2"],
            "item_id": ["item_A", "item_B"],
            "date": ["2025-01-01", "2025-01-02"],
            "sales": [10, 20],
            "feature_1": [1.0, 2.0],
            "feature_2": [100, 200],
            "feature_cat": ["A", "B"]
        })

    def test_separates_features_and_target(self, sample_df: pd.DataFrame):
        """Test that X and y are correctly separated."""
        X, y = prepare_features_target(sample_df, target_col="sales")
        assert "sales" not in X.columns
        assert all(col in X.columns for col in ["feature_1", "feature_2", "feature_cat"])
        assert y.name == "sales"
        pd.testing.assert_series_equal(y, pd.Series([10, 20], name="sales"))

    def test_excludes_identifier_columns(self, sample_df: pd.DataFrame):
        """Test that identifier columns are correctly excluded from features."""
        exclude_cols = ["id", "item_id", "date"]
        X, _ = prepare_features_target(sample_df)
        for col in exclude_cols:
            assert col not in X.columns

    def test_converts_object_to_category(self, sample_df: pd.DataFrame):
        """Test that object-type columns are converted to category for LightGBM."""
        X, _ = prepare_features_target(sample_df)
        assert X["feature_cat"].dtype == "category"
        assert X["feature_1"].dtype != "category"
