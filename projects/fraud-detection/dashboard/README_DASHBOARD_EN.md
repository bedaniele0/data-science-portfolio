# 💳 Fraud Detection Dashboard - User Guide

## 📊 System Information
**Developed by**: Eng. Daniel Varela Perez
**Email**: bedaniele0@gmail.com
**Phone**: +52 55 4189 3428
**Date**: September 24, 2025

---

## 🎯 General Description

The Fraud Detection Dashboard is an interactive web application built with **Streamlit** that provides a comprehensive graphical interface for the banking fraud detection system. It enables individual analysis, batch processing, real-time monitoring, and advanced system configuration.

---

## 🚀 Installation and Configuration

### Prerequisites
```bash
# Install dependencies
pip install streamlit plotly pandas numpy scikit-learn joblib

# Or use requirements.txt
pip install -r requirements.txt
```

### Required Files
- `models/improved_recall_threshold_model.pkl` (optimized model)
- `models/threshold_config.json` (threshold configuration)
- `dashboard/fraud_detection_dashboard.py` (main application)

### Launch
```bash
# Option 1: Automatic script
python run_dashboard.py

# Option 2: Manual launch
streamlit run dashboard/fraud_detection_dashboard.py --server.port 8501
```

### Access
- **URL**: http://localhost:8501
- **Port**: 8501 (configurable)

---

## 📱 Dashboard Features

### 🔍 **Tab 1: Individual Prediction**

**Purpose**: Analyze individual transactions in real-time.

**Features**:
- ✅ Intuitive data entry form
- ✅ Sample data for quick testing
- ✅ Real-time adjustable threshold
- ✅ Probability gauge visualization
- ✅ Main features analysis
- ✅ Automatic recommendations

**Usage**:
1. Enter transaction data (amount, PCA variables)
2. Adjust threshold if necessary (default: 0.300)
3. Click "Analyze Transaction"
4. Review results: gauge, metrics, recommendations

**Input Example**:
- Amount: $1500.00
- V1: -2.5, V2: 3.1, V3: -1.8
- Threshold: 0.30

**Expected Output**:
- Fraud Probability: 85.2%
- Prediction: FRAUD
- Risk Level: HIGH

### 📈 **Tab 2: Batch Analysis**

**Purpose**: Process multiple transactions simultaneously.

**Features**:
- ✅ CSV file upload
- ✅ Demo data generation (10-1000 transactions)
- ✅ Processing with progress bar
- ✅ Automatic distribution charts
- ✅ Dynamic result filters
- ✅ CSV results download

**Required CSV Format**:
```csv
Amount,V1,V2,V3,V4,V5,...,V28
150.00,-1.2,2.3,-0.8,1.1,-0.5,...,0.2
2500.00,-3.1,4.2,-2.1,2.8,-1.9,...,1.1
```

**Calculated Metrics**:
- Total processed transactions
- Number of detected frauds
- Batch fraud rate
- Average risk score

### 📊 **Tab 3: Real-Time Metrics**

**Purpose**: Monitor the system continuously.

**Features**:
- ✅ Auto-refresh every 5 seconds (optional)
- ✅ Real-time KPIs (24 hours)
- ✅ Hourly trend charts
- ✅ Automatic alert system
- ✅ Model statistics
- ✅ Risk score distribution

**Monitored KPIs**:
- Transactions per hour
- Detected frauds
- Average fraud rate
- Model response time

**Alert System**:
- 🟡 **Medium Alert**: >3 frauds in last hour
- 🔴 **High Alert**: Fraud rate >0.5%

### ⚙️ **Tab 4: Configuration**

**Purpose**: Adjust system parameters.

**Features**:
- ✅ Dynamic threshold adjustment
- ✅ Metrics impact estimation
- ✅ Detailed model information
- ✅ Maintenance tools
- ✅ Connection test

**Threshold Adjustment**:
- **Low (0.10)**: More sensitive, detects more frauds, more false alarms
- **Optimal (0.30)**: Ideal precision-recall balance
- **High (0.50)**: Less sensitive, fewer false alarms, may miss frauds

---

## 🎯 Main Use Cases

### 1. **Suspicious Transaction Analysis**
```
Scenario: Customer reports unrecognized charge
Process:
1. "Individual Prediction" tab
2. Enter transaction data
3. Review probability and risk level
4. Follow system recommendations
```

### 2. **Overnight Batch Processing**
```
Scenario: Batch analysis of all daily transactions
Process:
1. "Batch Analysis" tab
2. Upload CSV with daily transactions
3. Process with standard threshold
4. Download detected fraud report
5. Send to investigation team
```

### 3. **Operational Monitoring**
```
Scenario: Supervisor monitoring fraudulent activity
Process:
1. "Real-Time Metrics" tab
2. Activate auto-refresh
3. Monitor KPIs and alerts
4. Investigate suspicious activity spikes
```

### 4. **Sensitivity Adjustment**
```
Scenario: Too many false alarms reported
Process:
1. "Configuration" tab
2. Increase threshold (e.g.: 0.30 → 0.35)
3. Review estimated impact
4. Save new configuration
5. Monitor results for 1-2 days
```

---

## 📊 Performance Metrics

### Current System (Threshold 0.30)
- **Precision**: 93.62%
- **Recall**: 72.13%
- **F1-Score**: 81.48%
- **Accuracy**: 99.96%

### Comparison vs Validation
- Stable metrics between validation and test (no significant changes)

---

## 🛠️ Troubleshooting

### Common Issues

**1. Error: "Could not load model"**
```
Solution:
- Verify that exists: models/improved_recall_threshold_model.pkl
- If it doesn't exist, run notebooks 03 and 04
- Check file read permissions
```

**2. Dashboard doesn't load**
```
Solution:
- Verify port 8501 is available
- Install dependencies: pip install streamlit plotly
- Use script: python run_dashboard.py
```

**3. Batch analysis error**
```
Solution:
- Verify correct CSV format
- Ensure columns V1-V28 are present
- Check valid numeric values
```

**4. Real-time metrics don't update**
```
Solution:
- Activate "Automatic Update" checkbox
- Manually refresh page
- Check internet connection
```

### Logs and Debugging

**Enable detailed logs**:
```bash
streamlit run dashboard/fraud_detection_dashboard.py --logger.level debug
```

**Check model status**:
- "Configuration" tab → "Connection Test"

---

## 🔧 Advanced Customization

### Modify Default Thresholds
```python
# In fraud_detection_dashboard.py, line ~45
config = {'best_threshold': 0.30}  # Change value
```

### Add New Metrics
```python
# In Tab 3, add new KPIs
new_metric = calculate_custom_metric(data)
st.metric("New Metric", new_metric)
```

### Customize Alerts
```python
# Modify alert thresholds
if fraud_rate > 0.3:  # Change from 0.5 to 0.3
    alerts.append({'type': 'HIGH', 'message': '...'})
```

---

## 📈 Future Roadmap

### Planned Features
- ✨ **Real banking API integration**
- ✨ **Automatic email/SMS alerts**
- ✨ **Responsive mobile dashboard**
- ✨ **Machine Learning drift detection**
- ✨ **A/B model comparison**
- ✨ **Automatic PDF reports**

### Technical Improvements
- 🔧 **Database connection**
- 🔧 **Distributed cache for scalability**
- 🔧 **Authentication and user roles**
- 🔧 **Centralized logging**

---

## 💡 Best Practices

### For Analysts
1. **Review daily alerts** in Tab 3
2. **Adjust threshold monthly** based on feedback
3. **Process overnight batches** for complete analysis
4. **Document special cases** for model improvement

### For Administrators
1. **Monitor performance metrics** weekly
2. **Backup configurations** before changes
3. **Test new thresholds** in pilot mode
4. **Train users** on proper usage

### For Developers
1. **Update models** quarterly
2. **Monitor error logs** daily
3. **Optimize performance** according to volume
4. **Implement new features** based on feedback

---

## 📞 Support and Contact

### Technical Support
**Eng. Daniel Varela Perez**
- 📧 **Email**: bedaniele0@gmail.com
- 📱 **Phone**: +52 55 4189 3428
- 💼 **LinkedIn**: [Professional Profile]

### Support Hours
- **Monday to Friday**: 9:00 AM - 6:00 PM (GMT-6)
- **Emergencies**: 24/7 (critical cases only)
- **Average response**: <4 business hours

### Additional Documentation
- 📚 **Technical Manual**: `/docs/technical_manual.pdf`
- 🎥 **Tutorial Videos**: `/docs/video_tutorials/`
- 📖 **API Reference**: `/docs/api_reference.md`

---

**🎉 Dashboard ready for production use!**

*Developed with ❤️ by Eng. Daniel Varela Perez*
