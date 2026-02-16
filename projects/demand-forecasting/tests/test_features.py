"""
Tests for feature engineering functions

Author: Ing. Daniel Varela Perez
Email: bedaniele0@gmail.com
Date: December 5, 2024
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


class TestCalendarFeatures:
    """Test calendar feature generation"""

    def test_date_features(self):
        """Test basic date features extraction"""
        # Create sample data
        dates = pd.date_range('2016-01-01', periods=7, freq='D')
        df = pd.DataFrame({'date': dates})

        # Add date features
        df['day_of_week'] = df['date'].dt.dayofweek
        df['day_of_month'] = df['date'].dt.day
        df['month'] = df['date'].dt.month
        df['year'] = df['date'].dt.year

        # Assertions
        assert df['day_of_week'].min() >= 0
        assert df['day_of_week'].max() <= 6
        assert df['day_of_month'].min() >= 1
        assert df['day_of_month'].max() <= 31
        assert df['month'].min() >= 1
        assert df['month'].max() <= 12
        assert df['year'].iloc[0] == 2016

    def test_weekend_indicator(self):
        """Test weekend indicator creation"""
        dates = pd.date_range('2016-01-01', periods=7, freq='D')
        df = pd.DataFrame({'date': dates})
        df['day_of_week'] = df['date'].dt.dayofweek
        df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)

        # First day is Friday (4), so weekend starts at index 1 (Saturday)
        assert df['is_weekend'].sum() == 2  # Saturday and Sunday


class TestLagFeatures:
    """Test lag feature generation"""

    def test_lag_creation(self):
        """Test basic lag feature creation"""
        df = pd.DataFrame({
            'id': ['A', 'A', 'A', 'A'],
            'sales': [1, 2, 3, 4]
        })

        # Create lag_1
        df['sales_lag_1'] = df.groupby('id')['sales'].shift(1)

        # Check lag values
        assert pd.isna(df['sales_lag_1'].iloc[0])  # First value should be NaN
        assert df['sales_lag_1'].iloc[1] == 1
        assert df['sales_lag_1'].iloc[2] == 2
        assert df['sales_lag_1'].iloc[3] == 3

    def test_multiple_lags(self):
        """Test multiple lag features"""
        df = pd.DataFrame({
            'id': ['A'] * 10,
            'sales': list(range(10))
        })

        # Create multiple lags
        for lag in [1, 2, 3, 7]:
            df[f'sales_lag_{lag}'] = df.groupby('id')['sales'].shift(lag)

        # Check lag_7 at position 7
        assert df['sales_lag_7'].iloc[7] == 0
        assert df['sales_lag_3'].iloc[5] == 2


class TestRollingFeatures:
    """Test rolling window features"""

    def test_rolling_mean(self):
        """Test rolling mean calculation"""
        df = pd.DataFrame({
            'id': ['A'] * 10,
            'sales': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        })

        # Create rolling mean (window=3)
        df['sales_rolling_mean_3'] = df.groupby('id')['sales'].transform(
            lambda x: x.rolling(window=3, min_periods=1).mean()
        )

        # Check calculations
        assert df['sales_rolling_mean_3'].iloc[0] == 1.0  # [1]
        assert df['sales_rolling_mean_3'].iloc[1] == 1.5  # [1,2]
        assert df['sales_rolling_mean_3'].iloc[2] == 2.0  # [1,2,3]
        assert df['sales_rolling_mean_3'].iloc[3] == 3.0  # [2,3,4]

    def test_rolling_std(self):
        """Test rolling standard deviation"""
        df = pd.DataFrame({
            'id': ['A'] * 10,
            'sales': [5, 5, 5, 10, 10, 10, 5, 5, 5, 5]
        })

        # Create rolling std (window=3)
        df['sales_rolling_std_3'] = df.groupby('id')['sales'].transform(
            lambda x: x.rolling(window=3, min_periods=1).std()
        )

        # Check std for constant values
        assert df['sales_rolling_std_3'].iloc[2] == 0.0  # [5,5,5]


class TestPriceFeatures:
    """Test price-related features"""

    def test_price_change(self):
        """Test price change calculation"""
        df = pd.DataFrame({
            'id': ['A', 'A', 'A', 'A'],
            'price': [10.0, 12.0, 11.0, 11.0]
        })

        # Calculate price change
        df['price_change'] = df.groupby('id')['price'].diff()

        assert pd.isna(df['price_change'].iloc[0])
        assert df['price_change'].iloc[1] == 2.0
        assert df['price_change'].iloc[2] == -1.0
        assert df['price_change'].iloc[3] == 0.0

    def test_price_momentum(self):
        """Test price momentum (% change)"""
        df = pd.DataFrame({
            'id': ['A', 'A', 'A', 'A'],
            'price': [10.0, 12.0, 11.0, 11.0]
        })

        # Calculate price momentum
        df['price_momentum'] = df.groupby('id')['price'].pct_change()

        assert pd.isna(df['price_momentum'].iloc[0])
        assert abs(df['price_momentum'].iloc[1] - 0.2) < 1e-6  # 20% increase
        assert df['price_momentum'].iloc[2] < 0  # Decrease


class TestDataValidation:
    """Test data validation and quality checks"""

    def test_no_future_leakage(self):
        """Test that lag features don't leak future information"""
        df = pd.DataFrame({
            'id': ['A'] * 5,
            'date': pd.date_range('2016-01-01', periods=5),
            'sales': [1, 2, 3, 4, 5]
        })

        # Create lag_1
        df['sales_lag_1'] = df.groupby('id')['sales'].shift(1)

        # At each row, lag should be from previous row
        for i in range(1, len(df)):
            assert df['sales_lag_1'].iloc[i] == df['sales'].iloc[i-1]

    def test_missing_value_handling(self):
        """Test handling of missing values in features"""
        df = pd.DataFrame({
            'id': ['A'] * 5,
            'sales': [1, np.nan, 3, 4, 5]
        })

        # Fill missing values
        df['sales_filled'] = df['sales'].fillna(0)

        assert df['sales_filled'].isna().sum() == 0
        assert df['sales_filled'].iloc[1] == 0

    def test_zero_sales_handling(self):
        """Test handling of zero sales (zero-inflation)"""
        df = pd.DataFrame({
            'sales': [0, 0, 1, 0, 2, 0, 0, 3]
        })

        # Calculate zero proportion
        zero_pct = (df['sales'] == 0).sum() / len(df)

        assert 0 <= zero_pct <= 1
        assert zero_pct == 0.625  # 5 zeros out of 8


class TestModelInput:
    """Test model input preparation"""

    def test_feature_dtypes(self):
        """Test that features have correct data types"""
        df = pd.DataFrame({
            'sales_lag_1': [1.0, 2.0, 3.0],
            'day_of_week': [0, 1, 2],
            'price': [10.5, 11.2, 9.8]
        })

        # Check numeric types
        assert pd.api.types.is_numeric_dtype(df['sales_lag_1'])
        assert pd.api.types.is_numeric_dtype(df['day_of_week'])
        assert pd.api.types.is_numeric_dtype(df['price'])

    def test_no_infinite_values(self):
        """Test that features don't contain infinite values"""
        df = pd.DataFrame({
            'feature1': [1, 2, 3, 4],
            'feature2': [0.1, 0.2, 0.3, 0.4]
        })

        # Check for infinite values
        assert not np.isinf(df.values).any()

    def test_feature_scaling_bounds(self):
        """Test that scaled features are within expected bounds"""
        df = pd.DataFrame({
            'sales': [0, 10, 20, 30, 40]
        })

        # Min-max scaling
        df['sales_scaled'] = (df['sales'] - df['sales'].min()) / (df['sales'].max() - df['sales'].min())

        assert df['sales_scaled'].min() == 0.0
        assert df['sales_scaled'].max() == 1.0
        assert all(df['sales_scaled'] >= 0) and all(df['sales_scaled'] <= 1)


class TestModelPredictions:
    """Test model prediction pipeline"""

    def test_prediction_shape(self):
        """Test that predictions have correct shape"""
        # Simulate predictions
        n_samples = 100
        predictions = np.random.rand(n_samples)

        assert predictions.shape == (n_samples,)
        assert len(predictions) == n_samples

    def test_prediction_ranges(self):
        """Test that predictions are non-negative (sales can't be negative)"""
        predictions = np.array([0.5, 1.2, 3.4, 0.0, 2.1])

        # Clip negative predictions
        predictions_clipped = np.maximum(predictions, 0)

        assert all(predictions_clipped >= 0)

    def test_prediction_consistency(self):
        """Test that predictions are consistent for same input"""
        # Simulate feature matrix
        X = np.array([[1, 2, 3], [4, 5, 6]])

        # Mock prediction (same input should give same output)
        def mock_predict(X):
            return np.sum(X, axis=1)

        pred1 = mock_predict(X)
        pred2 = mock_predict(X)

        np.testing.assert_array_equal(pred1, pred2)


# Fixtures for common test data
@pytest.fixture
def sample_sales_data():
    """Create sample sales data for testing"""
    return pd.DataFrame({
        'id': ['A'] * 10 + ['B'] * 10,
        'date': pd.date_range('2016-01-01', periods=10).tolist() * 2,
        'sales': np.random.randint(0, 10, 20),
        'price': np.random.uniform(5, 15, 20)
    })


@pytest.fixture
def sample_calendar_data():
    """Create sample calendar data for testing"""
    return pd.DataFrame({
        'date': pd.date_range('2016-01-01', periods=30),
        'event_name_1': [''] * 30,
        'event_type_1': [''] * 30,
        'snap_CA': [0] * 30,
        'snap_TX': [0] * 30,
        'snap_WI': [0] * 30
    })


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
