# Production ML Portfolio — Daniel Varela Perez
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white) ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white) ![MLflow](https://img.shields.io/badge/MLflow-0194E2?logo=mlflow&logoColor=white) ![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)

Portfolio for **Senior ML Engineer / Applied Scientist (Production ML)** roles: reproducible pipelines, API/batch deployment, monitoring (drift + performance), and runbook-driven operations.

## Contact
- Name: Daniel Varela Perez
- Location: Mexico City, MX
- Email: bedaniele0@gmail.com
- Phone: +52 55 4189 3428
- GitHub: https://github.com/bedaniele0
- LinkedIn: https://linkedin.com/in/daniel-varela-perez
- 1-page CV: [ES MD](cv/CV_Daniel_Varela_Perez_1P_ES.md) | [EN MD](cv/CV_Daniel_Varela_Perez_1P_EN.md) | [ES ATS PDF](cv/CV_Daniel_Varela_Perez_1P_ES_ATS.pdf) | [EN ATS PDF](cv/CV_Daniel_Varela_Perez_1P_EN_ATS.pdf)

## Profile
Senior ML Engineer / Applied Scientist (Production ML) with end-to-end focus: design, validation, deployment (API/batch), and operational monitoring (drift + performance). Emphasis on reliability, traceability, and clear runbooks. Domains (churn/fraud/risk/forecasting) are used to demonstrate operational capability.

## Featured Gallery
<img src="assets/images/fraud-dashboard-1.png" style="width:100%; max-width:100%; height:auto;" alt="Fraud dashboard 1">
<em>Fraud — model overview</em><br>
<img src="assets/images/fraud-dashboard-2.png" style="width:100%; max-width:100%; height:auto;" alt="Fraud dashboard 2">
<em>Fraud — detailed metrics</em><br>
<img src="assets/images/credit-risk-dashboard-1.png" style="width:100%; max-width:100%; height:auto;" alt="Credit risk dashboard 1">
<em>Credit risk — threshold analysis</em><br>
<img src="assets/images/credit-risk-dashboard-2.png" style="width:100%; max-width:100%; height:auto;" alt="Credit risk dashboard 2">
<em>Credit risk — feature importance</em><br>
<img src="assets/images/walmart-dashboard-1.png" style="width:100%; max-width:100%; height:auto;" alt="Walmart dashboard 1">
<em>Walmart Forecasting — KPIs</em><br>
<img src="assets/images/walmart-dashboard-2.png" style="width:100%; max-width:100%; height:auto;" alt="Walmart dashboard 2">
<em>Walmart Forecasting — predictions</em><br>

## Architecture (Production ML)
<img src="assets/images/architecture.svg" style="width:100%; max-width:100%; height:auto;" alt="Production ML architecture">
<em>From data to operations: validation → training → registry → serving/batch → monitoring → runbooks</em><br>

## Live Demo
- ✅ Fraud Detection (Streamlit): https://bedaniele0-fraud-dete-dashboardfraud-detection-dashboard-lvseck.streamlit.app/
- Local demo commands for each project (API + dashboard / batch) are documented in `projects/*/README.md` (using `make`)

**Availability:** open to remote roles.

## Featured (Top 3)
1) **Fraud Detection System (E2E)** — Fraud detection with API + dashboard.  
   - Metrics: ROC-AUC 95.28% | Precision 93.62% | Recall 72.13%  
   - ROI demo: potential savings ~$25.9M/year (conservative ~$7.8M)  
   - Repo: `projects/fraud-detection`
   - Case Study (1 page): `projects/fraud-detection/CASE_STUDY.md`

2) **Credit Risk Scoring (E2E)** — Credit scoring with calibration and cost-based threshold.  
   - Metrics: AUC 78.13% | KS 42.51% | Recall 87.04% | Brier 0.1349  
   - Repo: `projects/credit-risk`
   - Case Study (1 page): `projects/credit-risk/CASE_STUDY.md`

3) **Walmart Demand Forecasting (E2E)** — Retail forecasting with pipeline + API/dashboard.  
   - Metrics: MAE 0.6845 | RMSE 3.9554 | MAPE 52.75% (batch N=28,000)  
   - ROI demo: ~$467K/year (10 stores)  
   - Repo: `projects/demand-forecasting`
   - Case Study (1 page): `projects/demand-forecasting/CASE_STUDY.md`

## Additional References (1 line each)
- Note: Reference demo projects focused on results. Full code available on request.
- `projects/powergrid-forecast` — Energy forecasting | MAPE 5.10% | R2 0.9555
- `projects/diabetes-prediction` — Medical classification | AUC 84.14% | Recall 74.07%
- `projects/churn-prediction` — Churn | AUC 83.80% | Recall 92.51%
- `projects/retail-inventory` — Inventory | MAE 6,937 | RMSE 24,318
- `projects/olist-retention` — Retention | AUC 99.50% | Recall 96.40%
- `projects/telco-churn` — Telco churn | AUC 83.20% | F1 62.40%
- `projects/user-score` — Batch E2E | MAE on target | R2 to improve

<details>
<summary>All Projects (10) - KPI Snapshot</summary>

| Project | Type | KPI 1 | KPI 2 | KPI 3 |
|---|---|---:|---:|---:|
| `projects/fraud-detection` | Classification | ROC-AUC 95.28% | Precision 93.62% | Recall 72.13% |
| `projects/credit-risk` | Classification | AUC 78.13% | KS 42.51% | Recall 87.04% |
| `projects/demand-forecasting` | Regression | MAE 0.6845 | RMSE 3.9554 | MAPE 52.75% (batch N=28,000) |
| `projects/powergrid-forecast` | Regression | MAPE 5.10% | R2 0.9555 | MAE 319.88 kW |
| `projects/diabetes-prediction` | Classification | AUC 84.14% | Accuracy 78.57% | Recall 74.07% |
| `projects/churn-prediction` | Classification | AUC 83.80% | Recall 92.51% | Precision 42.51% |
| `projects/retail-inventory` | Regression | MAE 6,937 | RMSE 24,318 | R2 0.119 |
| `projects/olist-retention` | Classification | AUC 99.50% | Precision 99.70% | Recall 96.40% |
| `projects/telco-churn` | Classification | AUC 83.20% | F1 62.40% | ROI 4.56x |
| `projects/user-score` | Regression | MAE on target | R2 to improve | Batch E2E |

Each project includes local demo commands and technical/executive documentation.

</details>
