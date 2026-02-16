# PHASE 1: SQL AND EXPLORATORY ANALYSIS - EXECUTIVE SUMMARY

## 📊 Project Information
**Developed by**: Eng. Daniel Varela Perez
**Email**: bedaniele0@gmail.com
**Phone**: +52 55 4189 3428
**Date**: September 24th, 2025
**Phase**: 1 - SQL EDA Analysis

---

## 🎯 OBJECTIVE COMPLETED
Perform deep analysis using SQL to identify fraud patterns in banking transactions from the creditcard.csv dataset containing 284,807 transactions.

## 📈 MAIN DATASET METRICS

### General Distribution
- **Total transactions**: 284,807
- **Normal transactions**: 284,315 (99.8273%)
- **Fraudulent transactions**: 492 (0.1727%)
- **Imbalance ratio**: 578.9:1 (Normal:Fraud)

### Amount Statistics
| Class | Average | Q25 | Median | Q75 | Maximum |
|-------|---------|-----|--------|-----|---------|
| Normal | $88.29 | $5.65 | $22.00 | $77.05 | $25,691.16 |
| Fraud | $122.21 | $1.00 | $9.25 | $105.89 | $2,125.87 |

## 🔍 IDENTIFIED FRAUD PATTERNS

### 1. **Zero Amount Pattern**
- **Finding**: Zero amount transactions have 1.48% fraud rate
- **Implication**: 8.5x higher than average rate
- **Recommendation**: Create specific rule for zero amount transactions

### 2. **High Amount Pattern**
- **Finding**: $500-$1000 range has 0.42% fraud rate
- **Implication**: 2.4x higher than average rate
- **Recommendation**: Special monitoring for high amount transactions

### 3. **Predictive Correlations**
- **V3**: -0.1930 (strongest correlation)
- **V4**: +0.1334 (second strongest)
- **V1**: -0.1013 (third strongest)

### 4. **Temporal Distribution**
- **Day 1**: 281 frauds out of 144,786 total transactions
- **Day 2**: 211 frauds out of 140,021 total transactions
- **Pattern**: Relatively uniform distribution over time

### 5. **Amount Range Analysis**
```
Range            | Total    | Frauds | Rate
Zero (0)         | 1,825    | 27      | 1.48%
Very_Low (0-10)  | 98,439   | 222     | 0.23%
Low (10-50)      | 90,781   | 57      | 0.06%
Medium (50-100)  | 37,254   | 56      | 0.15%
High (100-500)   | 47,366   | 95      | 0.20%
Very_High (500+) | 9,142    | 35      | 0.38%
```

## 🚀 RECOMMENDATIONS FOR ML MODELING

### Balancing Techniques
1. **SMOTE** (Synthetic Minority Oversampling Technique)
2. **ADASYN** (Adaptive Synthetic Sampling)
3. **Strategic undersampling** of majority class
4. **Cost-sensitive learning** with class weights

### Priority Evaluation Metrics
- ✅ **Precision**: Minimize false positives
- ✅ **Recall**: Maximize fraud detection
- ✅ **F1-Score**: Balance between precision and recall
- ✅ **AUC-ROC**: General discrimination capability
- ✅ **AUC-PR**: Especially important for imbalanced data
- ❌ **Accuracy**: Do not use as main metric

### Recommended Algorithms
1. **XGBoost** - Excellent for imbalanced data
2. **LightGBM** - Fast and efficient
3. **Random Forest** - With class_weight='balanced'
4. **Ensemble Methods** - Combination of multiple models

### Suggested Feature Engineering
- **Velocity Features**: Number of transactions per time window
- **Temporal aggregations**: Statistics per hour/day
- **Interactions**: Combinations between variables V1-V28
- **Percentiles**: Relative position of amounts
- **Ratios**: Relationships between existing variables

### Validation
- **StratifiedKFold** to maintain class distribution
- **Time-based split** if temporal component is important
- **Hold-out set** completely separate for final evaluation

## 📊 GENERATED DELIVERABLES

### Created Files
1. **📓 Notebook**: `notebooks/01_sql_eda_analysis.ipynb`
2. **🗂️ SQL Queries**: `data/sql/analysis_queries.sql`
3. **📊 Visualization**: `reports/figures/sql_analysis_complete.png`
4. **📋 Results**: `reports/sql_eda_results_complete.json`
5. **🐍 Executable script**: `run_sql_analysis.py`

### Main SQL Queries
- Distribution of frauds vs normals
- Statistics by transaction amount
- Temporal analysis with time buckets
- Feature engineering with window functions
- Anomalous pattern detection
- Correlation analysis

## 🎯 BUSINESS OBJECTIVES FOR NEXT PHASE

### Suggested Target Metrics
- **Precision > 99.5%**: Minimize impact on legitimate customers
- **Recall > 85%**: Detect majority of frauds
- **False Positives < 0.5%**: Reduce operational friction
- **Inference Time < 100ms**: Real-time decisions

## ✅ PHASE 1 SUCCESSFULLY COMPLETED

**Status**: ✅ **COMPLETE**
**Next step**: Phase 2 - Feature Engineering and ML Modeling
**Preparation**: Dataset analyzed, patterns identified, strategy defined

---
**Developed by**: Eng. Daniel Varela Perez | Email: bedaniele0@gmail.com | Tel: +52 55 4189 3428