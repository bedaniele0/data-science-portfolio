import pytest
import pandas as pd
import os

DATA_PATH = os.path.join("data", "processed", "train_clean.parquet", "part.0.parquet")

def test_processed_data_exists():
    assert os.path.exists(DATA_PATH), f"Archivo no encontrado: {DATA_PATH}"

def test_no_nulls_in_processed_data():
    df = pd.read_parquet(DATA_PATH)
    assert df.isnull().sum().sum() == 0, "Hay valores nulos en los datos procesados"

def test_expected_columns_exist():
    df = pd.read_parquet(DATA_PATH)
    expected_cols = 41  # Actualizado desde 30
    assert df.shape[1] == expected_cols, f"Se esperaban {expected_cols} columnas, se encontraron {df.shape[1]}"
