# Model Card - Walmart Demand Forecasting LightGBM

**Autor**: Ing. Daniel Varela Perez
**Email**: bedaniele0@gmail.com
**Tel**: +52 55 4189 3428
**Fecha**: 5 de Diciembre, 2024
**Versión**: 1.0

---

## Model Details

### Basic Information

- **Model Name**: Walmart Demand Forecasting - LightGBM
- **Model Version**: 1.2.0
- **Model Type**: Gradient Boosting Machine (LightGBM)
- **Framework**: LightGBM 4.5.0
- **Task**: Time Series Forecasting (Regression)
- **Language**: Python 3.10+
- **License**: MIT
- **Date Created**: December 5, 2024
- **Model File**: `models/lightgbm_model.pkl` (297 KB)

### Model Description

This model predicts daily sales for Walmart product-store combinations using a LightGBM gradient boosting algorithm. The model was trained on historical sales data from the M5 Forecasting Competition, incorporating 88 engineered features including temporal patterns, price dynamics, events, and lagged sales information.

### Intended Use

**Primary Use Case**:
- Forecast daily sales for individual products across 10 Walmart stores
- Support inventory planning and optimization decisions
- Reduce stockouts and excess inventory

**Intended Users**:
- Supply chain managers
- Inventory planners
- Store operations teams
- Data science teams

**Out-of-Scope Use Cases**:
- Long-term strategic planning (>28 days)
- New products without historical data
- Store locations not in the training data
- Non-retail forecasting applications

---

## Training Data

### Dataset

- **Source**: M5 Forecasting Competition (Kaggle)
- **Period**: 2011-01-29 to 2016-04-24 (1,913 days)
- **Training Period**: 2011-01-29 to 2016-03-27 (1,885 days)
- **Validation Period**: 2016-03-28 to 2016-04-24 (28 days)
- **Number of Series**: 30,490 (product × store combinations)
- **Total Training Observations**: 1,885,000
- **Total Validation Observations**: 28,000

### Data Characteristics

- **Stores**: 10 stores across 3 states (CA, TX, WI)
- **Products**: 3,049 unique items
- **Categories**:
  - FOODS (63.5% of data)
  - HOUSEHOLD (23.3%)
  - HOBBIES (13.2%)
- **Zero-Inflation**: 68.2% of observations are zero sales
- **Average Daily Sales**: 1.9 units (non-zero: 5.9 units)

### Features

**Total Features**: 88 engineered features

**Feature Categories**:
1. **Calendar Features** (~20): Day of week, month, year, holidays, days to events
2. **Price Features** (~15): Current price, price changes, price momentum, relative pricing
3. **Event Features** (~15): SNAP benefits, special events, promotional indicators
4. **Lag Features** (6): Sales lag 1, 2, 3, 7, 14, 28 days
5. **Rolling Features** (~32): Rolling mean, std, min, max (7, 14, 28 day windows)

**Top 5 Most Important Features**:
1. `sales_rolling_mean_7` (importance: 509)
2. `sales_lag_3` (importance: 292)
3. `sales_lag_2` (importance: 240)
4. `sales_lag_1` (importance: 237)
5. `day_of_week` (importance: 187)

---

## Model Architecture

### Algorithm

**LightGBM** (Light Gradient Boosting Machine)
- Tree-based ensemble learning method
- Uses gradient boosting framework
- Optimized for efficiency and scalability

### Hyperparameters

```python
{
    'objective': 'regression',
    'metric': 'mae',
    'boosting_type': 'gbdt',
    'num_leaves': 31,
    'learning_rate': 0.05,
    'feature_fraction': 0.9,
    'bagging_fraction': 0.8,
    'bagging_freq': 5,
    'verbose': -1,
    'n_estimators': 500,
    'random_state': 42
}
```

### Training Configuration

- **Early Stopping**: 50 rounds
- **Validation Strategy**: Time-based split (last 28 days)
- **Loss Function**: Mean Absolute Error (MAE)
- **Training Time**: ~45 seconds
- **Memory Usage**: ~2.5 GB during training

---

## Performance Metrics

### Overall Performance (Validation Set)

**Nota:** esta sección se basa en evaluación batch histórica (N=28,000). Para métricas recientes del dashboard (muestra n=1,000), ver `README.md`.

| Metric | Baseline (Naive) | Moving Average | **Our Model** | Improvement |
|--------|------------------|----------------|---------------|-------------|
| **MAE** | 0.9748 | 0.7101 | **0.6845** | **29.78%** vs baseline |
| **RMSE** | 5.9302 | 3.7500 | **3.9554** | **33.29%** vs baseline |
| **MAPE** | 85.35% | 55.02% | **52.75%** | **38.20%** vs baseline |

### Performance by Category

| Category | MAE | RMSE | MAPE | N |
|----------|-----|------|------|---|
| **HOUSEHOLD** | 0.5056 | 1.2075 | 49.55% | 9,100 |
| **HOBBIES** | 0.6100 | 1.6666 | 60.82% | 5,628 |
| **FOODS** | 0.8388 | 5.5524 | 52.16% | 13,272 |

**Key Insights**:
- HOUSEHOLD category easiest to predict (lowest MAE)
- FOODS category most challenging (highest variance)
- HOBBIES has highest MAPE due to intermittent demand

### Performance by Store

| Store | State | MAE | RMSE | N |
|-------|-------|-----|------|---|
| **TX_3** | TX | 0.5469 | 1.2225 | 2,464 |
| **CA_4** | CA | 0.5808 | 1.3416 | 3,248 |
| **WI_1** | WI | 0.5846 | 1.3266 | 2,520 |
| **WI_2** | WI | 0.5990 | 1.2364 | 2,800 |
| **WI_3** | WI | 0.6187 | 2.3561 | 2,744 |
| **CA_1** | CA | 0.7025 | 1.3339 | 2,296 |
| **TX_1** | TX | 0.7029 | 10.0635 | 3,584 |
| **CA_2** | CA | 0.7184 | 1.7062 | 3,080 |
| **TX_2** | TX | 0.7485 | 1.8037 | 2,492 |
| **CA_3** | CA | 1.0372 | 2.7175 | 2,772 |

**Key Insights**:
- Texas store TX_3 has best performance
- California store CA_3 has highest error (potential data quality issues)
- Store-specific factors significantly impact accuracy

### Temporal Performance

- **Mean Daily MAE**: 0.6845
- **Median Daily MAE**: 0.6753
- **Std Daily MAE**: 0.0980
- **Min Daily MAE**: 0.5584
- **Max Daily MAE**: 1.0245

Model shows stable performance across validation period with no significant drift.

---

## Limitations

### Known Limitations

1. **Zero-Inflated Data**:
   - 68.2% of observations are zero sales
   - Model may underpredict for rare events
   - MAPE metric unreliable for zero-sales items

2. **Category Imbalance**:
   - FOODS category has higher error (MAE: 0.84)
   - Possible improvement with category-specific models

3. **Outlier Handling**:
   - High RMSE vs MAE ratio indicates outlier sensitivity
   - Top 10 worst predictions concentrated in FOODS category
   - Residuals show high skewness (118.87)

4. **Data Leakage Risk**:
   - Careful feature engineering required for production
   - Lag features must be computed correctly in real-time

5. **Cold Start Problem**:
   - Model requires historical data (minimum 28 days)
   - Cannot predict for new products without history

### Edge Cases

- **Promotional Events**: May underestimate spike in demand
- **Stock-outs**: Historical zero sales may be actual stock-outs (missing data issue)
- **New Products**: Requires alternative approach (category-level forecasting)
- **Seasonality**: Validation period limited to 28 days (seasonal patterns not fully validated)

---

## Ethical Considerations

### Fairness

- **Geographic Bias**: Model trained on 3 US states (CA, TX, WI) only
- **Product Bias**: Performance varies significantly by category
- **No demographic data**: Model does not use customer demographic information

### Privacy

- **No PII**: Model uses only aggregated sales data
- **No customer data**: Individual customer information not used
- **Store-level aggregation**: All data at store-product-day level

### Potential Harms

- **Over-ordering**: False positives could lead to excess inventory and waste
- **Under-ordering**: False negatives could lead to stockouts and lost sales
- **Job displacement**: Automation may reduce manual forecasting jobs

### Mitigation Strategies

- Human-in-the-loop validation for high-value items
- Confidence intervals for uncertainty quantification
- Regular model retraining to capture evolving patterns
- A/B testing before full deployment

---

## Business Impact

### Quantified Benefits (demo, trazable a MAE)

**Accuracy Improvement**:
- 29.78% MAE reduction vs naive baseline
- 33.29% RMSE reduction vs naive baseline

**Impacto económico derivado del error (demo)**:
- Fórmula: `Costo ≈ MAE × precio_prom × items_por_tienda × días × tiendas`
- Supuestos conservadores:
  - Precio promedio: **$4.41**
  - Ítems forecast por tienda/día: **100**
  - Tiendas: **10**
  - Días: **365**

| Concepto | MAE | Costo anual (USD) |
|----------|-----|-------------------|
| Baseline (naive) | 0.9748 | 1,569,121 |
| Modelo LightGBM | 0.6845 | 1,101,873 |
| **Ahorro anual** | — | **467,249** |

> Este ROI demo está anclado a métricas reales de validación.  
> En producción puede variar según mix de SKUs, precios y niveles de servicio.

### Key Business Benefits

✓ Reduced stockouts (better demand prediction)
✓ Lower inventory holding costs
✓ Improved customer satisfaction
✓ Better promotional planning
✓ Automated forecasting pipeline (time savings)

---

## Deployment Considerations

### Model Serving

- **Model Size**: 297 KB (lightweight, fast loading)
- **Inference Time**: <100ms per batch of 1,000 predictions
- **Memory Requirements**: <500 MB in production
- **Feature Computation**: ~2 seconds for 1,000 items
- **Recommended Infrastructure**:
  - CPU: 4 cores minimum
  - RAM: 8 GB minimum
  - Storage: 10 GB for features + model

### Retraining Schedule

**Recommended Frequency**: Weekly

**Triggers for Retraining**:
- Weekly scheduled retraining (incorporate latest data)
- MAE degradation >10% vs baseline
- Significant business events (store openings, category changes)
- Seasonality changes (quarterly review)

### Monitoring Requirements

**Key Metrics to Monitor**:
1. **Performance Metrics**: Daily MAE, RMSE by category/store
2. **Data Quality**: Missing values, outliers, distribution shifts
3. **Prediction Distribution**: Mean, std, min, max predictions
4. **Feature Drift**: Track feature distribution changes
5. **Business Metrics**: Actual stockout rate, inventory levels

**Alert Thresholds**:
- MAE exceeds baseline + 10%
- Missing data >5%
- Prediction outliers >3 std deviations
- Feature distribution shift >20%

---

## Model Card Authors

**Primary Author**: Ing. Daniel Varela Perez
**Affiliation**: Independent Data Scientist
**Contact**: bedaniele0@gmail.com

**Reviewers**: N/A (awaiting peer review)

---

## Model Card Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024-12-05 | Initial model card creation |
| 1.2.0 | 2025-12-23 | Actualización de versión y nota sobre métricas dashboard vs batch |
| 1.3.0 | 2026-02-06 | Actualización de estado y referencias de monitoreo (F8/F9) |

---

## Additional Resources

### Documentation

- **Project Repository**: [GitHub](#)
- **Problem Statement**: `docs/00_problem_statement.md`
- **Architecture Design**: `docs/02_design_architecture.md`
- **Feature Catalog**: `docs/04_feature_catalog.md`
- **EDA Report**: `docs/03_eda_report.md`
- **Notebooks Alignment**: `docs/NOTEBOOKS_ALIGNMENT.md`

### Experiments

- **MLflow Tracking**: `mlruns/` directory
- **Feature Importance**: `models/feature_importance_lgb.csv`
- **Model Comparison**: `models/model_comparison.csv`
- **Evaluation Reports**: `reports/` directory

### Notebooks

- `01_eda.ipynb` - Exploratory Data Analysis
- `02_feature_engineering.ipynb` - Feature engineering pipeline
- `03_baseline_modeling.ipynb` - Baseline models
- `04_advanced_modeling.ipynb` - LightGBM training
- `05_evaluation.ipynb` - Comprehensive evaluation

---

## Glossary

- **MAE** (Mean Absolute Error): Average absolute difference between predicted and actual values
- **RMSE** (Root Mean Squared Error): Square root of average squared differences
- **MAPE** (Mean Absolute Percentage Error): Average percentage error
- **SNAP**: Supplemental Nutrition Assistance Program (affects food sales)
- **Zero-Inflation**: High proportion of zero sales in time series data
- **Feature Importance**: Metric showing which features contribute most to predictions
- **Gradient Boosting**: Ensemble learning method that builds trees sequentially

---

## Citation

If you use this model, please cite:

```bibtex
@misc{walmart_forecasting_lgb_2024,
  author = {Varela Perez, Daniel},
  title = {Walmart Demand Forecasting with LightGBM},
  year = {2024},
  publisher = {GitHub},
  howpublished = {\url{https://github.com/yourusername/walmart-demand-forecasting}},
  note = {Model Card v1.2.0}
}
```

---

**Model Card Last Updated**: February 6, 2026
**Model Card Version**: 1.3.0
**Model Status**: ✅ Demo-ready / Architecture-ready (API usa features mock en demo)

---

*This model card follows the format proposed by Mitchell et al. (2019) and Google's Model Card Toolkit guidelines.*
