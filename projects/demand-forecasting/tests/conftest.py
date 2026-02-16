"""
Pytest configuration and shared fixtures

Author: Ing. Daniel Varela Perez
Email: bedaniele0@gmail.com
Date: December 5, 2024
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path


@pytest.fixture(scope='session')
def project_root():
    """Get project root directory"""
    return Path(__file__).parent.parent


@pytest.fixture(scope='session')
def data_dir(project_root):
    """Get data directory path"""
    return project_root / 'data'


@pytest.fixture(scope='session')
def models_dir(project_root):
    """Get models directory path"""
    return project_root / 'models'


@pytest.fixture
def sample_sales_series():
    """Generate a sample sales time series"""
    np.random.seed(42)
    dates = pd.date_range('2016-01-01', periods=100, freq='D')
    sales = np.random.poisson(lam=3, size=100)  # Poisson distribution for sales

    return pd.DataFrame({
        'date': dates,
        'sales': sales
    })


@pytest.fixture
def sample_features():
    """Generate sample feature matrix"""
    np.random.seed(42)
    n_samples = 1000

    return pd.DataFrame({
        'sales_lag_1': np.random.rand(n_samples) * 10,
        'sales_lag_7': np.random.rand(n_samples) * 10,
        'sales_rolling_mean_7': np.random.rand(n_samples) * 10,
        'day_of_week': np.random.randint(0, 7, n_samples),
        'month': np.random.randint(1, 13, n_samples),
        'price': np.random.uniform(5, 15, n_samples),
        'is_weekend': np.random.randint(0, 2, n_samples)
    })


@pytest.fixture
def sample_predictions():
    """Generate sample predictions and actuals"""
    np.random.seed(42)
    n = 100

    y_true = np.random.poisson(lam=3, size=n)
    y_pred = y_true + np.random.normal(0, 1, n)  # Add some noise
    y_pred = np.maximum(y_pred, 0)  # Clip negative values

    return y_true, y_pred


@pytest.fixture
def empty_dataframe():
    """Create an empty DataFrame with expected columns"""
    return pd.DataFrame(columns=['id', 'date', 'sales', 'price'])


# Configure pytest
def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )
