"""
Tests for ModelService covering inference and metadata paths.

Autor: Ing. Daniel Varela Perez
Email: bedaniele0@gmail.com
Fecha: December 13, 2024
"""

import pandas as pd

from src.api.model_service import ModelService, get_model_service


class TestModelService:
    def test_model_info_fields(self):
        svc = get_model_service()
        info = svc.model_info()

        required = [
            "model_name",
            "model_version",
            "model_type",
            "model_path",
            "features_count",
            "loaded_at",
            "is_loaded",
        ]
        for field in required:
            assert field in info

    def test_feature_importance_returns_records(self):
        svc = get_model_service()
        records = svc.feature_importance(top_n=5)
        assert isinstance(records, list)
        if records:  # optional depending on model
            assert "feature" in records[0]
            assert "importance" in records[0]

    def test_predict_from_request_with_existing_item(self):
        svc = get_model_service()
        # Use an item/date known to exist in demo features (suffix normalized internally)
        y_hat = svc.predict_from_request(
            item_id="FOODS_1_001_CA_1",
            store_id="CA_1",
            date="2016-05-01",
        )
        assert isinstance(y_hat, float)
        assert y_hat >= 0

    def test_is_ready_confirms_feature_base(self):
        svc = get_model_service()
        ready, detail = svc.is_ready()
        assert isinstance(ready, bool)
        assert isinstance(detail, str)
