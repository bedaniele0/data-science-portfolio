# Diseño Arquitectónico - Walmart Demand Forecasting

**Autor**: Ing. Daniel Varela Perez
**Email**: bedaniele0@gmail.com
**Tel**: +52 55 4189 3428
**Fecha**: 4 de Diciembre, 2024
**Versión**: 1.0
**Proyecto**: Walmart Demand Forecasting & Inventory Optimization

---

## 📋 FASE 2: DISEÑO ARQUITECTÓNICO (DVP-PRO)

---

## 1. Resumen Ejecutivo

Este documento describe la arquitectura objetivo para un sistema de forecasting de demanda. El diseño prioriza escalabilidad, modularidad y reproducibilidad. En el estado actual (demo/portafolio) se implementa un subconjunto funcional para ejecución local.

**Incluye (demo actual):**
- **Procesamiento** del dataset M5 con features (lags, calendar, prices, eventos, SNAP)
- **Predicciones** con modelo LightGBM preentrenado (local)
- **API REST** con endpoints `/`, `/health`, `/info`, `/model/info`, `/model/features/importance`, `/predict`, `/predict/batch`
- **Dashboard** Streamlit para visualizaciones y KPIs
- **MLflow** opcional en local para tracking de experimentos

**Planeado (fuera de demo):**
- Retraining automatizado y pipelines programados
- Monitoreo continuo y alertas productivas
- Optimización de inventario y políticas de reabastecimiento
- Deployment containerizado y escalado horizontal

---

## 2. Arquitectura General del Sistema

### 2.1 Vista de Alto Nivel

```
┌─────────────────────────────────────────────────────────────────────┐
│                         DATA SOURCES                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│  │  Sales   │  │ Calendar │  │  Prices  │  │ External │            │
│  │   CSV    │  │   CSV    │  │   CSV    │  │   Data   │            │
│  └─────┬────┘  └─────┬────┘  └─────┬────┘  └─────┬────┘            │
└────────┼─────────────┼─────────────┼─────────────┼─────────────────┘
         │             │             │             │
         └─────────────┴─────────────┴─────────────┘
                       │
         ┌─────────────▼─────────────┐
         │   DATA INGESTION LAYER    │
         │  • Validation             │
         │  • Schema checks          │
         │  • Format conversion      │
         └─────────────┬─────────────┘
                       │
         ┌─────────────▼─────────────┐
         │   DATA PROCESSING LAYER   │
         │  • ETL Pipeline           │
         │  • Feature Engineering    │
         │  • Data Quality checks    │
         └─────────────┬─────────────┘
                       │
         ┌─────────────▼─────────────┐
         │   FEATURE STORE           │
         │  • Processed features     │
         │  • Version control        │
         │  • Metadata catalog       │
         └─────────────┬─────────────┘
                       │
         ┌─────────────▼─────────────┐
         │   ML TRAINING LAYER       │
         │  • Model training         │
         │  • Hyperparameter tuning  │
         │  • Cross-validation       │
         │  • MLflow tracking        │
         └─────────────┬─────────────┘
                       │
         ┌─────────────▼─────────────┐
         │   MODEL REGISTRY          │
         │  • Best models            │
         │  • Version history        │
         │  • Metadata & metrics     │
         └─────────────┬─────────────┘
                       │
         ┌─────────────▼─────────────┐
         │   INFERENCE LAYER         │
         │  • Batch predictions      │
         │  • Real-time API          │
         │  • Optimization module    │
         └─────────────┬─────────────┘
                       │
         ┌─────────────▼─────────────┐
         │   SERVING LAYER           │
         │  • FastAPI REST API       │
         │  • Streamlit Dashboard    │
         │  • Result storage         │
         └─────────────┬─────────────┘
                       │
         ┌─────────────▼─────────────┐
         │   MONITORING LAYER        │
         │  • Model drift detection  │
         │  • Performance metrics    │
         │  • Alerting system        │
         └───────────────────────────┘
```

### 2.2 Artefactos y contratos actuales (demo)
- **Procesamiento**: `src/data/make_dataset.py` → `data/processed/dataset.parquet` (wide → long + lags/rolling)
- **Feature store local**: `data/processed/sales_with_features.parquet`, `data/processed/valid_data.csv`, `data/processed/valid_data.parquet`
- **Modelos**: `models/lightgbm_model.pkl` + `models/feature_importance_lgb.csv`
- **Serving**: FastAPI (`src/api/main.py`) con fallback de inferencia para fechas/ids fuera de cobertura; respuestas incluyen `predicted_sales`, `model_version`, `timestamp`
- **Dashboard**: Streamlit `src/visualization/dashboard.py`
- **Orquestación**: `Makefile` targets `train`, `predict`, `api`, `dashboard`, `mlflow-ui`

---

## 3. Arquitectura de Datos

### 3.1 Data Pipeline (ETL)

```
┌─────────────────────────────────────────────────────────────────┐
│                     DATA PIPELINE FLOW                           │
└─────────────────────────────────────────────────────────────────┘

  [RAW DATA]
      │
      ├── sales_train_validation.csv (114 MB)
      ├── calendar.csv (101 KB)
      ├── sell_prices.csv (194 MB)
      │
      ▼
  [VALIDATION]
      │
      ├─► Schema validation (pandera)
      ├─► Data type checks
      ├─► Completeness checks
      ├─► Range validation
      │
      ▼
  [CLEANING]
      │
      ├─► Handle missing values
      ├─► Remove duplicates
      ├─► Outlier treatment
      ├─► Type casting
      │
      ▼
  [TRANSFORMATION]
      │
      ├─► Date parsing & formatting
      ├─► Hierarchical structure
      ├─► Wide to long format
      ├─► ID generation
      │
      ▼
  [FEATURE ENGINEERING]
      │
      ├─► Lag features (1, 7, 28 days)
      ├─► Rolling statistics (7, 14, 28, 90 days)
      ├─► Calendar features (dow, month, holiday)
      ├─► Price features (current, changes, momentum)
      ├─► SNAP indicators
      ├─► Event encoding
      │
      ▼
  [FEATURE STORE]
      │
      ├─► data/processed/sales_with_features.parquet
      ├─► data/processed/valid_data.parquet
      ├─► data/processed/feature_catalog.txt
      │
      ▼
  [VERSIONING]
      │
      └─► Git LFS / DVC (for large files)
```

### 3.2 Estructura de Datos

#### **Tabla Principal: Sales (Long Format)**
```sql
CREATE TABLE sales_data (
    id VARCHAR(100),              -- Unique identifier
    date DATE,                    -- Transaction date
    store_id VARCHAR(10),         -- Store identifier (CA_1, TX_2, etc.)
    item_id VARCHAR(20),          -- Item identifier
    dept_id VARCHAR(20),          -- Department ID
    cat_id VARCHAR(20),           -- Category ID
    state_id VARCHAR(5),          -- State (CA, TX, WI)
    sales INTEGER,                -- Units sold (TARGET)
    sell_price DECIMAL(10,2),     -- Price
    snap_flag BOOLEAN,            -- SNAP eligible
    event_name VARCHAR(50),       -- Event name
    event_type VARCHAR(20)        -- Event type
);
```

#### **Tabla de Features (Engineered)**
```sql
CREATE TABLE features_engineered (
    id VARCHAR(100),
    date DATE,

    -- Lag features
    sales_lag_1 INTEGER,
    sales_lag_7 INTEGER,
    sales_lag_28 INTEGER,

    -- Rolling statistics
    sales_rolling_mean_7 DECIMAL(10,2),
    sales_rolling_std_7 DECIMAL(10,2),
    sales_rolling_mean_28 DECIMAL(10,2),
    sales_rolling_std_28 DECIMAL(10,2),

    -- Calendar features
    day_of_week INTEGER,
    day_of_month INTEGER,
    week_of_year INTEGER,
    month INTEGER,
    quarter INTEGER,
    is_weekend BOOLEAN,
    is_month_start BOOLEAN,
    is_month_end BOOLEAN,

    -- Price features
    price_current DECIMAL(10,2),
    price_change_pct DECIMAL(10,4),
    price_momentum DECIMAL(10,4),

    -- Event features
    has_event BOOLEAN,
    event_type_encoded INTEGER,
    days_to_event INTEGER,

    -- Target
    target INTEGER
);
```

---

## 4. Arquitectura de ML Pipeline

### 4.1 Training Pipeline

```
┌────────────────────────────────────────────────────────────┐
│                    ML TRAINING PIPELINE                     │
└────────────────────────────────────────────────────────────┘

  [FEATURE STORE]
      │
      ▼
  [DATA PREPARATION]
      │
      ├─► Train/Validation/Test split (temporal)
      ├─► Scaling (StandardScaler, MinMaxScaler)
      ├─► Encoding (OrdinalEncoder for categories)
      │
      ▼
  [BASELINE MODELS]
      │
      ├─► Naive Forecast
      ├─► Seasonal Naive
      ├─► Moving Average
      ├─► Exponential Smoothing
      │
      ▼
  [STATISTICAL MODELS]
      │
      ├─► ARIMA / SARIMA
      ├─► Prophet (Meta)
      ├─► ETS (Error-Trend-Seasonal)
      │
      ▼
  [ML MODELS]
      │
      ├─► Linear Regression
      ├─► Ridge / Lasso
      ├─► Random Forest
      ├─► XGBoost
      ├─► LightGBM ⭐ (Primary)
      ├─► CatBoost
      │
      ▼
  [DEEP LEARNING] (Opcional)
      │
      ├─► LSTM
      ├─► GRU
      ├─► N-BEATS
      │
      ▼
  [HYPERPARAMETER TUNING]
      │
      ├─► Optuna optimization
      ├─► Bayesian optimization
      ├─► Grid/Random search
      │
      ▼
  [ENSEMBLE]
      │
      ├─► Weighted average
      ├─► Stacking
      ├─► Hierarchical reconciliation
      │
      ▼
  [VALIDATION]
      │
      ├─► Time-series CV
      ├─► Walk-forward validation
      ├─► Final test set evaluation
      │
      ▼
  [MODEL SELECTION]
      │
      └─► Best model → Model Registry
```

**Nota demo**: en el estado actual se utiliza LightGBM con features diseñadas; los bloques de modelos estadísticos, deep learning, ensembles y reconciliación jerárquica quedan como línea base para evolución.

### 4.2 MLflow Tracking Structure (opcional en demo)

```
mlruns/
├── 0/                          # Default experiment
├── 1/                          # Baseline models
│   ├── run_001/               # Naive
│   ├── run_002/               # Seasonal Naive
│   └── run_003/               # Moving Average
├── 2/                          # Statistical models
│   ├── run_001/               # ARIMA
│   ├── run_002/               # Prophet
│   └── run_003/               # ETS
├── 3/                          # ML models
│   ├── run_001/               # XGBoost
│   ├── run_002/               # LightGBM
│   └── run_003/               # CatBoost
└── 4/                          # Ensemble models
    └── run_001/               # Final ensemble

Each run contains:
├── artifacts/
│   ├── model/                 # Serialized model
│   ├── features/              # Feature list
│   ├── plots/                 # Visualizations
│   └── metrics/               # Evaluation metrics
├── params/                     # Hyperparameters
├── metrics/                    # Performance metrics
└── tags/                       # Metadata tags
```

---

## 5. Arquitectura de Deployment

**Nota demo**: la ejecución actual es local (FastAPI + Streamlit). La sección siguiente describe un despliegue containerizado objetivo.

### 5.1 Componentes del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                    DEPLOYMENT ARCHITECTURE                   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                        CONTAINER 1                           │
│                       API SERVICE                            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  FastAPI Application                                 │   │
│  │  ├── /predict (POST)       - Single prediction      │   │
│  │  ├── /predict/batch (POST) - Batch predictions      │   │
│  │  ├── /health (GET)         - Health check           │   │
│  │  ├── /model/info (GET)     - Model info             │   │
│  │  ├── /model/features/importance (GET) - Importancia │   │
│  │  └── /docs (GET)           - Swagger documentation  │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  Port: 8000                                                  │
│  Workers: 4 (Gunicorn)                                       │
│  Timeout: 60s                                                │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                        CONTAINER 2                           │
│                    DASHBOARD SERVICE                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Streamlit Application                               │   │
│  │  ├── Home - Overview & KPIs                          │   │
│  │  ├── Forecasting - Predictions & charts             │   │
│  │  ├── Inventory - Optimization recommendations       │   │
│  │  ├── Performance - Model metrics & drift            │   │
│  │  └── Data - Raw data exploration                    │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  Port: 8501                                                  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                        SHARED VOLUMES                        │
│  ├── /models      - Trained models                          │
│  ├── /data        - Processed data                          │
│  └── /logs        - Application logs                        │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 Docker Architecture

```yaml
# docker-compose.yml structure

services:
  api:
    image: walmart-forecasting-api:latest
    ports: ["8000:8000"]
    volumes:
      - ./models:/app/models:ro
      - ./data:/app/data:ro
      - ./logs:/app/logs
    environment:
      - MODEL_PATH=/app/models/best_model.pkl
      - LOG_LEVEL=INFO
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  dashboard:
    image: walmart-forecasting-dashboard:latest
    ports: ["8501:8501"]
    depends_on:
      - api
    environment:
      - API_URL=http://api:8000
    volumes:
      - ./data:/app/data:ro
      - ./reports:/app/reports

  # Optional: Monitoring
  prometheus:
    image: prom/prometheus
    ports: ["9090:9090"]
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    ports: ["3000:3000"]
    depends_on:
      - prometheus
```

---

## 6. API Design

### 6.1 Endpoints Specification

#### **POST /predict**
**Descripción**: Predicción para un producto-tienda específico (1 fecha)

**Request Body**:
```json
{
  "item_id": "FOODS_1_001_CA_1",
  "store_id": "CA_1",
  "date": "2016-05-01"
}
```

**Response**:
```json
{
  "item_id": "FOODS_1_001_CA_1",
  "store_id": "CA_1",
  "date": "2016-05-01",
  "predicted_sales": 3.45,
  "prediction_interval": {
    "lower": 2.10,
    "upper": 4.80
  },
  "model_version": "1.0.0",
  "timestamp": "2024-12-05T15:30:00Z"
}
```

#### **POST /predict/batch**
**Descripción**: Predicciones para múltiples productos-tiendas (una fecha por item)

**Request Body**:
```json
{
  "items": [
    {"item_id": "FOODS_1_001_CA_1", "store_id": "CA_1", "date": "2016-05-01"},
    {"item_id": "FOODS_1_002_CA_1", "store_id": "CA_1", "date": "2016-05-01"}
  ]
}
```

#### **GET /model/info**
**Descripción**: Metadata del modelo en uso.

#### **GET /model/features/importance**
**Descripción**: Importancia de variables del modelo.

---

## 7. Módulos del Sistema

### 7.1 Módulo de Data Processing

**Ubicación**: `src/data/`

```
src/data/
├── __init__.py
└── make_dataset.py        # Pipeline de preparación y splits
```

**Funciones principales**:
- Generación de dataset en formato long
- Split temporal train/valid/test

### 7.2 Módulo de Feature Engineering

**Ubicación**: `src/features/`

```
src/features/
├── __init__.py
├── build_features.py      # Pipeline principal
├── lag_features.py        # Lag features (1, 7, 28 días)
├── rolling_features.py    # Rolling statistics
├── calendar_features.py   # Temporal features
├── price_features.py      # Price-based features
├── event_features.py      # Event encoding
└── feature_selector.py    # Feature selection
```

**Clases principales**:
- `FeatureEngineer` - Pipeline completo
- `LagFeatureGenerator` - Genera lag features
- `RollingFeatureGenerator` - Rolling stats
- `FeatureSelector` - Selección de features

### 7.3 Módulo de Modeling

**Ubicación**: `src/models/`

```
src/models/
├── __init__.py
├── train_demand.py        # Training script
├── predict.py             # Inference script
├── evaluate.py            # Metrics & validation
└── mlflow_utils.py        # Tracking helpers
```

### 7.4 Módulo de Optimization (no implementado en demo)

**Estado**: definido para versión enterprise; no forma parte del demo.

```
src/optimization/
├── __init__.py
├── inventory_optimizer.py  # Optimización principal
├── eoq_calculator.py       # Economic Order Quantity
├── safety_stock.py         # Safety stock calculation
├── service_level.py        # Service level optimization
└── cost_calculator.py      # Cost analysis
```

### 7.5 Módulo de API

**Ubicación**: `src/api/`

```
src/api/
├── __init__.py
├── main.py                # FastAPI app
├── model_service.py       # Carga de modelo y features
└── schemas.py             # Pydantic schemas
```

### 7.6 Módulo de Dashboard

**Ubicación**: `src/visualization/`

```
src/visualization/
├── __init__.py
└── dashboard.py           # Streamlit main app
```

---

## 8. Architecture Decision Records (ADRs)

### ADR-001: Elección de LightGBM como modelo principal

**Fecha**: 2024-12-04
**Status**: Accepted

**Contexto**:
Necesitamos un modelo ML escalable para 30,490 series temporales con buen balance entre precisión y velocidad.

**Decisión**:
Usaremos **LightGBM** como modelo principal de forecasting.

**Razones**:
1. **Performance**: Superior a XGBoost en datasets grandes
2. **Velocidad**: 10-20x más rápido que XGBoost
3. **Memoria**: Eficiente en uso de memoria
4. **Features**: Manejo nativo de categóricas
5. **Comunidad**: Ampliamente usado en competencias de forecasting

**Alternativas consideradas**:
- **XGBoost**: Más lento, mayor uso de memoria
- **Prophet**: Bueno para series individuales, no escala bien
- **LSTM**: Requiere GPU, más complejo de mantener

**Consecuencias**:
- ✅ Training más rápido
- ✅ Menor uso de memoria
- ✅ Facilidad de deployment
- ⚠️ Requiere feature engineering manual (vs DL automático)

---

### ADR-002: FastAPI para API REST

**Fecha**: 2024-12-04
**Status**: Accepted

**Contexto**:
Necesitamos API REST con baja latencia (<100ms) y documentación automática.

**Decisión**:
Usaremos **FastAPI** para la API de predicción.

**Razones**:
1. **Performance**: Basado en Starlette (async)
2. **Validación**: Pydantic para validación de datos
3. **Documentación**: Swagger UI automático
4. **Type hints**: Support completo para Python type hints
5. **Moderno**: Framework más moderno vs Flask

**Alternativas**:
- **Flask**: Más maduro pero síncrono y más lento
- **Django REST**: Overhead innecesario para nuestro caso

**Consecuencias**:
- ✅ Latencia <100ms garantizada
- ✅ Documentación auto-generada
- ✅ Validación robusta de inputs
- ⚠️ Curva de aprendizaje para async programming

---

### ADR-003: Streamlit para Dashboard

**Fecha**: 2024-12-04
**Status**: Accepted

**Contexto**:
Necesitamos dashboard interactivo para stakeholders no técnicos.

**Decisión**:
Usaremos **Streamlit** para el dashboard de visualización.

**Razones**:
1. **Simplicidad**: Desarrollo rápido en Python puro
2. **Interactividad**: Widgets interactivos out-of-the-box
3. **Integración**: Fácil integración con pandas/plotly
4. **Deployment**: Deployment simple

**Alternativas**:
- **Dash (Plotly)**: Más flexible pero más complejo
- **Gradio**: Enfocado en ML demos, menos customizable

**Consecuencias**:
- ✅ Desarrollo 3x más rápido
- ✅ Mantenimiento simple
- ⚠️ Menos customizable que Dash
- ⚠️ Performance limitado para datasets muy grandes

---

### ADR-004: Docker para Deployment

**Fecha**: 2024-12-04
**Status**: Accepted

**Contexto**:
Necesitamos deployment reproducible en cualquier ambiente.

**Decisión**:
Usaremos **Docker** + **docker-compose** para containerización.

**Razones**:
1. **Reproducibilidad**: Mismo ambiente en dev/prod
2. **Portabilidad**: Corre en cualquier OS
3. **Aislamiento**: Dependencias encapsuladas
4. **Escalabilidad**: Fácil escalar horizontalmente

**Consecuencias**:
- ✅ Deployment consistente
- ✅ No hay "funciona en mi máquina"
- ⚠️ Overhead de contenedores
- ⚠️ Curva de aprendizaje Docker

---

### ADR-005: MLflow para Experiment Tracking

**Fecha**: 2024-12-04
**Status**: Accepted

**Contexto**:
Necesitamos tracking de experimentos, versionado de modelos y registro centralizado.

**Decisión**:
Usaremos **MLflow** para tracking y model registry.

**Razones**:
1. **Tracking**: Logging automático de params/metrics
2. **Registry**: Model registry con versionado
3. **Deployment**: Servicio de deployment integrado
4. **Framework-agnostic**: Funciona con cualquier framework ML
5. **Open-source**: Sin vendor lock-in

**Alternativas**:
- **Weights & Biases**: Mejor UI pero requiere cloud
- **Neptune**: Similar pero menos adoption

**Consecuencias**:
- ✅ Trazabilidad completa de experimentos
- ✅ Model registry centralizado
- ✅ Reproducibilidad garantizada
- ⚠️ Requiere SQLite/PostgreSQL para tracking

---

## 9. Estrategia de Versionado

### 9.1 Versionado de Código
- **Git**: Control de versiones de código
- **Semantic Versioning**: MAJOR.MINOR.PATCH
- **Branching**: GitFlow (main, develop, feature/*, hotfix/*)

### 9.2 Versionado de Datos
- **DVC** (Data Version Control) para datasets grandes
- **Git LFS** para archivos binarios medianos
- **Metadata files** (.json) con hash de datos

### 9.3 Versionado de Modelos
- **MLflow Model Registry**:
  - `None` → `Staging` → `Production` → `Archived`
- **Naming convention**: `lightgbm_v1.2.3_20241204`

### 9.4 Versionado de Features
- **Feature catalog** (JSON/YAML) con:
  - Feature name
  - Feature version
  - Generation logic
  - Dependencies
  - Statistics

---

## 10. Estrategia de Testing

### 10.1 Tests (demo)
```
tests/
├── test_api.py
├── test_features.py
├── test_model.py
├── test_model_service.py
└── test_train_demand_main.py
```

**Nota**: cobertura y tipos de pruebas pueden ampliarse en una fase productiva.

---

## 11. Monitoreo y Observabilidad

**Nota demo**: existen módulos base en `src/monitoring/`, pero no están integrados en un pipeline productivo.

### 11.1 Logging Strategy
```python
# Structured logging con loguru
logger.info("prediction_request", extra={
    "store_id": "CA_1",
    "item_id": "HOBBIES_1_001",
    "inference_time_ms": 45,
    "model_version": "1.0.0"
})
```

### 11.2 Métricas de Sistema
- **Latencia**: p50, p95, p99 de API requests
- **Throughput**: Requests/segundo
- **Error rate**: % de requests fallidos
- **Model performance**: MAE, RMSE tracking

### 11.3 Alertas
- Degradación de accuracy >10%
- Latencia >200ms
- Error rate >5%
- Data drift detected

---

## 12. Seguridad

### 12.1 API Security
- **Authentication**: API keys (Bearer token)
- **Rate limiting**: 100 requests/minute por cliente
- **Input validation**: Pydantic schemas
- **CORS**: Configurado para dominios específicos

### 12.2 Data Security
- **Sensitive data**: Encriptación at rest
- **Logs**: No almacenar PII en logs
- **Secrets**: Uso de .env files (no en Git)

---

## 13. Próximos Pasos

### Roadmap (posterior al demo)
1. ✅ Arquitectura definida
2. ✅ Data pipeline y feature engineering
3. ✅ Modelo LightGBM entrenado
4. ✅ API FastAPI + Dashboard Streamlit
5. ⏳ Automatizar retraining y jobs programados
6. ⏳ Integrar monitoreo y alertas
7. ⏳ Optimización de inventario
8. ⏳ Containerización y despliegue

---

## 14. Referencias

- **FastAPI**: https://fastapi.tiangolo.com/
- **LightGBM**: https://lightgbm.readthedocs.io/
- **MLflow**: https://mlflow.org/docs/latest/index.html
- **Streamlit**: https://docs.streamlit.io/
- **Docker**: https://docs.docker.com/

---

**Elaborado por**:
Ing. Daniel Varela Perez
Senior Data Scientist & ML Engineer
📧 bedaniele0@gmail.com
📱 +52 55 4189 3428

**Versión**: 1.0 - Diseño Arquitectónico Completo
**Fecha**: 4 de Diciembre, 2024

---

## Aprobaciones

- [ ] **Arquitectura de Datos**: Pendiente
- [ ] **Arquitectura de ML**: Pendiente
- [ ] **Arquitectura de Deployment**: Pendiente
- [ ] **Security Review**: Pendiente
- [ ] **Technical Lead**: Pendiente

**Status**: ✅ Documento completo y listo para implementación
