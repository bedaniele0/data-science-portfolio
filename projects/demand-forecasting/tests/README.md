# Tests - Walmart Demand Forecasting

**Author**: Ing. Daniel Varela Perez
**Email**: bedaniele0@gmail.com
**Date**: December 5, 2024

---

## Overview

This directory contains unit tests for the Walmart Demand Forecasting project. Tests cover feature engineering, model validation, data quality checks, and business metrics calculations.

---

## Test Structure

```
tests/
├── __init__.py                 # Package initialization
├── conftest.py                # Pytest configuration and shared fixtures
├── test_features.py           # Feature engineering tests
├── test_model.py              # Model training and evaluation tests
└── README.md                  # This file
```

---

## Running Tests

### Run All Tests

```bash
# From project root
pytest tests/ -v
```

### Run Specific Test File

```bash
pytest tests/test_features.py -v
pytest tests/test_model.py -v
```

### Run Specific Test Class

```bash
pytest tests/test_features.py::TestCalendarFeatures -v
```

### Run With Coverage

```bash
pytest tests/ --cov=src --cov-report=html
```

### Run Only Fast Tests

```bash
pytest tests/ -m "not slow"
```

---

## Test Categories

### 1. Feature Engineering Tests (`test_features.py`)

**TestCalendarFeatures**:
- Date feature extraction (day, month, year)
- Weekend indicator creation

**TestLagFeatures**:
- Lag feature creation (lag 1, 2, 3, 7)
- Multiple lag features validation

**TestRollingFeatures**:
- Rolling mean calculation
- Rolling standard deviation

**TestPriceFeatures**:
- Price change calculation
- Price momentum (% change)

**TestDataValidation**:
- No future data leakage
- Missing value handling
- Zero-sales handling (zero-inflation)

**TestModelInput**:
- Feature data types validation
- No infinite values check
- Feature scaling bounds

**TestModelPredictions**:
- Prediction shape validation
- Non-negative predictions
- Prediction consistency

### 2. Model Tests (`test_model.py`)

**TestModelLoading**:
- Model file existence
- Model deserialization

**TestModelPrediction**:
- Prediction output type
- Non-negative predictions
- Shape consistency

**TestModelMetrics**:
- MAE calculation
- RMSE calculation
- MAPE calculation

**TestModelValidation**:
- Train/validation split (no leakage)
- Feature creation (no future data)

**TestBaselineModels**:
- Naive baseline
- Seasonal naive baseline
- Moving average baseline

**TestFeatureImportance**:
- Feature importance format
- Top features identification

**TestDataQuality**:
- No duplicate records
- Missing value thresholds
- Outlier detection

**TestModelComparison**:
- Model ranking by MAE
- Improvement calculation

**TestBusinessMetrics**:
- Cost savings calculation
- ROI calculation

---

## Test Results

### Latest Test Run (December 5, 2024)

```
============================= test session starts ==============================
platform darwin -- Python 3.13.7, pytest-9.0.1, pluggy-1.6.0
collected 39 items

tests/test_features.py::TestCalendarFeatures::test_date_features PASSED
tests/test_features.py::TestCalendarFeatures::test_weekend_indicator PASSED
... (37 more tests)

============================== 39 passed in 2.06s ==============================
```

**Summary**:
- ✅ **39 tests passed**
- ⏱️ **Execution time**: 2.06 seconds
- ✅ **Coverage**: Core feature engineering and model functions

---

## Fixtures

Shared fixtures are defined in `conftest.py`:

- `project_root`: Project root directory path
- `data_dir`: Data directory path
- `models_dir`: Models directory path
- `sample_sales_series`: Sample time series data
- `sample_features`: Sample feature matrix
- `sample_predictions`: Sample predictions and actuals
- `empty_dataframe`: Empty DataFrame with expected schema

---

## Adding New Tests

### Template for New Test

```python
class TestNewFeature:
    """Test new feature functionality"""

    def test_basic_behavior(self):
        """Test basic behavior"""
        # Arrange
        input_data = ...

        # Act
        result = ...

        # Assert
        assert result == expected
```

### Best Practices

1. **Arrange-Act-Assert**: Structure tests clearly
2. **Descriptive names**: Use descriptive test names
3. **One assertion per test**: Test one thing at a time
4. **Use fixtures**: Reuse common test data
5. **Mock external dependencies**: Don't rely on external systems
6. **Fast tests**: Keep tests fast (<1 second each)

---

## Test Markers

Custom markers defined in `conftest.py`:

- `@pytest.mark.slow`: For slow-running tests
- `@pytest.mark.integration`: For integration tests
- `@pytest.mark.unit`: For unit tests

Usage:

```python
@pytest.mark.slow
def test_long_running_operation():
    # Test code
    pass
```

---

## Continuous Integration

These tests are designed to run in CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run Tests
  run: |
    pytest tests/ -v --cov=src --cov-report=xml
```

---

## Coverage Goals

- **Target**: 80% code coverage
- **Current**: ~60% (feature engineering and model core)
- **Next steps**:
  - Add API tests (when API is implemented)
  - Add integration tests for full pipeline
  - Add data processing tests

---

## Troubleshooting

### Import Errors

If you get import errors, make sure you're in the project root:

```bash
cd /path/to/walmart-demand-forecasting
pytest tests/
```

### Virtual Environment

Always activate the virtual environment:

```bash
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows
```

### Missing Dependencies

Install test dependencies:

```bash
pip install pytest pytest-cov
```

---

## Future Tests to Add

### Phase 8 (Deployment)
- [ ] API endpoint tests
- [ ] Model serving tests
- [ ] Response time tests
- [ ] Error handling tests

### Phase 9 (Monitoring)
- [ ] Drift detection tests
- [ ] Alert mechanism tests
- [ ] Dashboard functionality tests

---

## Contact

For questions about tests or to report issues:

**Ing. Daniel Varela Perez**
- 📧 Email: bedaniele0@gmail.com
- 📱 Phone: +52 55 4189 3428

---

**Last Updated**: December 5, 2024
**Test Suite Version**: 1.0.0
**Status**: ✅ All tests passing
