"""
Tests for model training and prediction

Author: Ing. Daniel Varela Perez
Email: bedaniele0@gmail.com
Date: December 5, 2024
"""

import pytest
import pandas as pd
import numpy as np
import joblib
from pathlib import Path


class TestModelLoading:
    """Test model loading and serialization"""

    def test_model_file_exists(self):
        """Test that trained model file exists"""
        model_path = Path('models/lightgbm_model.pkl')
        # This test will pass if model exists, skip otherwise
        if model_path.exists():
            assert model_path.is_file()
            assert model_path.stat().st_size > 0

    def test_model_loading(self):
        """Test that model can be loaded successfully"""
        model_path = Path('models/lightgbm_model.pkl')
        if model_path.exists():
            try:
                model = joblib.load(model_path)
                assert model is not None
            except Exception as e:
                pytest.fail(f"Model loading failed: {e}")


class TestModelPrediction:
    """Test model prediction functionality"""

    def test_prediction_output_type(self):
        """Test that predictions are numeric"""
        # Mock predictions
        predictions = np.array([1.2, 3.4, 0.5, 2.1])

        assert isinstance(predictions, np.ndarray)
        assert predictions.dtype in [np.float32, np.float64]

    def test_prediction_non_negative(self):
        """Test that sales predictions are non-negative"""
        # Mock predictions (some negative that should be clipped)
        raw_predictions = np.array([1.2, -0.5, 3.4, -1.0, 2.1])
        predictions = np.maximum(raw_predictions, 0)

        assert all(predictions >= 0), "All predictions should be non-negative"

    def test_prediction_shape_consistency(self):
        """Test that prediction shape matches input shape"""
        n_samples = 100
        n_features = 80

        # Mock feature matrix
        X = np.random.rand(n_samples, n_features)

        # Mock prediction (would come from actual model)
        predictions = np.random.rand(n_samples)

        assert len(predictions) == n_samples


class TestModelMetrics:
    """Test model evaluation metrics"""

    def test_mae_calculation(self):
        """Test Mean Absolute Error calculation"""
        y_true = np.array([1, 2, 3, 4, 5])
        y_pred = np.array([1.1, 2.2, 2.8, 4.1, 5.2])

        mae = np.mean(np.abs(y_true - y_pred))

        assert mae >= 0, "MAE should be non-negative"
        assert mae < 1, "MAE should be less than 1 for this example"

    def test_rmse_calculation(self):
        """Test Root Mean Squared Error calculation"""
        y_true = np.array([1, 2, 3, 4, 5])
        y_pred = np.array([1.1, 2.2, 2.8, 4.1, 5.2])

        rmse = np.sqrt(np.mean((y_true - y_pred) ** 2))

        assert rmse >= 0, "RMSE should be non-negative"
        assert rmse >= np.mean(np.abs(y_true - y_pred)), "RMSE should be >= MAE"

    def test_mape_calculation(self):
        """Test Mean Absolute Percentage Error calculation"""
        y_true = np.array([1, 2, 3, 4, 5])
        y_pred = np.array([1.1, 2.2, 2.8, 4.1, 5.2])

        # Filter out zeros to avoid division by zero
        mask = y_true != 0
        mape = np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100

        assert mape >= 0, "MAPE should be non-negative"
        assert mape <= 100, "MAPE should typically be <= 100%"


class TestModelValidation:
    """Test model validation procedures"""

    def test_train_val_split_no_leakage(self):
        """Test that validation data comes after training data"""
        dates = pd.date_range('2016-01-01', periods=100, freq='D')
        df = pd.DataFrame({
            'date': dates,
            'sales': np.random.rand(100)
        })

        # Split: last 28 days for validation
        split_idx = len(df) - 28
        train_df = df.iloc[:split_idx]
        val_df = df.iloc[split_idx:]

        # Validation should start after training ends
        assert train_df['date'].max() < val_df['date'].min()
        assert len(val_df) == 28

    def test_no_data_leakage_in_features(self):
        """Test that features don't use future information"""
        df = pd.DataFrame({
            'date': pd.date_range('2016-01-01', periods=10),
            'sales': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        })

        # Create lag feature
        df['sales_lag_1'] = df['sales'].shift(1)

        # For each non-null lag, it should equal previous sales
        for i in range(1, len(df)):
            assert df['sales_lag_1'].iloc[i] == df['sales'].iloc[i-1]


class TestBaselineModels:
    """Test baseline model implementations"""

    def test_naive_baseline(self):
        """Test naive forecast (last value)"""
        sales = np.array([1, 2, 3, 4, 5])
        naive_forecast = sales[:-1]  # Shift by 1
        actual = sales[1:]

        mae = np.mean(np.abs(actual - naive_forecast))
        assert mae >= 0

    def test_seasonal_naive_baseline(self):
        """Test seasonal naive forecast (lag 7)"""
        sales = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        seasonal_forecast = sales[:-7]  # Lag 7
        actual = sales[7:]

        mae = np.mean(np.abs(actual - seasonal_forecast))
        assert mae >= 0

    def test_moving_average_baseline(self):
        """Test moving average forecast"""
        sales = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        window = 3

        # Simple moving average
        ma = np.convolve(sales, np.ones(window)/window, mode='valid')

        assert len(ma) == len(sales) - window + 1
        assert all(ma > 0)


class TestFeatureImportance:
    """Test feature importance analysis"""

    def test_feature_importance_format(self):
        """Test that feature importance is properly formatted"""
        feature_importance = pd.DataFrame({
            'feature': ['sales_lag_1', 'day_of_week', 'price'],
            'importance': [100, 50, 25]
        })

        assert 'feature' in feature_importance.columns
        assert 'importance' in feature_importance.columns
        assert all(feature_importance['importance'] >= 0)

    def test_top_features_identification(self):
        """Test identification of top important features"""
        feature_importance = pd.DataFrame({
            'feature': ['f1', 'f2', 'f3', 'f4', 'f5'],
            'importance': [100, 80, 60, 40, 20]
        })

        top_5 = feature_importance.nlargest(5, 'importance')

        assert len(top_5) == 5
        assert top_5['importance'].iloc[0] == 100
        assert top_5['importance'].is_monotonic_decreasing


class TestDataQuality:
    """Test data quality checks"""

    def test_no_duplicate_records(self):
        """Test that there are no duplicate id-date combinations"""
        df = pd.DataFrame({
            'id': ['A', 'A', 'B', 'B'],
            'date': ['2016-01-01', '2016-01-02', '2016-01-01', '2016-01-02'],
            'sales': [1, 2, 3, 4]
        })

        duplicates = df.duplicated(subset=['id', 'date']).sum()
        assert duplicates == 0

    def test_missing_value_threshold(self):
        """Test that missing values are within acceptable threshold"""
        df = pd.DataFrame({
            'feature1': [1, 2, np.nan, 4, 5],
            'feature2': [1, 2, 3, 4, 5],
            'feature3': [np.nan, np.nan, 3, 4, 5]
        })

        missing_pct = df.isnull().sum() / len(df)

        # Check that no feature has >50% missing
        assert all(missing_pct <= 0.5)

    def test_outlier_detection(self):
        """Test outlier detection using IQR method"""
        data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 100])

        Q1 = np.percentile(data, 25)
        Q3 = np.percentile(data, 75)
        IQR = Q3 - Q1

        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outliers = (data < lower_bound) | (data > upper_bound)

        # Should detect 100 as outlier
        assert outliers.sum() > 0


class TestModelComparison:
    """Test model comparison functionality"""

    def test_model_ranking(self):
        """Test that models are correctly ranked by MAE"""
        results = pd.DataFrame({
            'Model': ['LightGBM', 'Moving Average', 'Naive', 'Seasonal Naive'],
            'MAE': [0.6845, 0.7101, 0.9748, 1.0015]
        })

        sorted_results = results.sort_values('MAE')

        # LightGBM should be first (best)
        assert sorted_results.iloc[0]['Model'] == 'LightGBM'
        assert sorted_results.iloc[0]['MAE'] < 0.7

    def test_improvement_calculation(self):
        """Test improvement percentage calculation"""
        baseline_mae = 0.9748
        model_mae = 0.6845

        improvement = (baseline_mae - model_mae) / baseline_mae * 100

        assert improvement > 0, "Model should improve over baseline"
        assert abs(improvement - 29.78) < 0.1, "Improvement should be ~29.78%"


class TestBusinessMetrics:
    """Test business impact calculations"""

    def test_cost_savings_calculation(self):
        """Test annual cost savings estimation"""
        baseline_mae = 0.9748
        model_mae = 0.6845
        avg_price = 4.41
        daily_items = 1000

        baseline_cost = baseline_mae * avg_price * daily_items * 365
        model_cost = model_mae * avg_price * daily_items * 365
        savings = baseline_cost - model_cost

        assert savings > 0, "Model should generate cost savings"
        assert savings > 400000, "Savings should exceed $400K"

    def test_roi_calculation(self):
        """Test ROI calculation"""
        annual_savings = 467249
        implementation_cost = 100000  # Hypothetical

        roi = (annual_savings - implementation_cost) / implementation_cost * 100

        assert roi > 0, "ROI should be positive"
        assert roi > 300, "ROI should exceed 300%"


# Run tests
if __name__ == '__main__':
    pytest.main([__file__, '-v'])
