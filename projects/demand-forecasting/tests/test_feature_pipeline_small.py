"""
Small-scope tests for FeatureEngineeringPipeline with synthetic data.

Objetivo: cubrir el flujo principal de build_features con un dataset mínimo
para validar que se generan columnas clave sin ejecutar el pipeline completo
de M5.

Autor: Ing. Daniel Varela Perez
Email: bedaniele0@gmail.com
Fecha: December 13, 2024
"""

import pandas as pd

from src.features.build_features import FeatureEngineeringPipeline


def _sample_sales_df():
    dates = pd.date_range("2016-01-01", periods=10, freq="D")
    return pd.DataFrame(
        {
            "id": ["FOODS_1_CA_1"] * 10,
            "item_id": ["FOODS_1_001"] * 10,
            "store_id": ["CA_1"] * 10,
            "cat_id": ["FOODS"] * 10,
            "wm_yr_wk": [11101 + i for i in range(10)],
            "date": dates,
            "sales": [1, 2, 0, 3, 2, 4, 5, 6, 3, 2],
        }
    )


def _sample_calendar_df():
    dates = pd.date_range("2016-01-01", periods=10, freq="D")
    return pd.DataFrame(
        {
            "date": dates,
            "event_name_1": [None] * 4 + ["SuperBowl"] + [None] * 5,
            "event_type_1": [None] * 4 + ["Sporting"] + [None] * 5,
            "event_name_2": [None] * 10,
            "event_type_2": [None] * 10,
            "snap_CA": [0, 1, 0, 1, 0, 0, 1, 0, 0, 0],
            "snap_TX": [0] * 10,
            "snap_WI": [0] * 10,
        }
    )


def _sample_prices_df():
    return pd.DataFrame(
        {
            "store_id": ["CA_1"] * 10,
            "item_id": ["FOODS_1_001"] * 10,
            "wm_yr_wk": [11101 + i for i in range(10)],
            "sell_price": [1.0, 1.1, 1.1, 1.2, 1.2, 1.2, 1.3, 1.3, 1.3, 1.4],
        }
    )


def test_feature_pipeline_generates_key_columns():
    df_sales = _sample_sales_df()
    df_calendar = _sample_calendar_df()
    df_prices = _sample_prices_df()

    pipeline = FeatureEngineeringPipeline()
    features = pipeline.run(
        df_sales=df_sales,
        df_calendar=df_calendar,
        df_prices=df_prices,
        include_advanced=False,
    )

    expected_cols = [
        "sales_lag_1",
        "sales_rolling_mean_7",
        "price_change_pct",
        "is_event",
        "snap_CA",
    ]
    for col in expected_cols:
        assert col in features.columns

    # No data leakage: first lag should be NaN
    assert pd.isna(features["sales_lag_1"].iloc[0])

    # Event flag should trigger on the event day
    event_day = features.loc[features["event_name_1"].notna()]
    if not event_day.empty:
        assert (event_day["is_event"] == 1).all()
