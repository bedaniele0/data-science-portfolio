# ============================================================================
# Makefile - Walmart Demand Forecasting
# ============================================================================
# Automatización de tareas comunes del proyecto
#
# Autor: Ing. Daniel Varela Perez
# Email: bedaniele0@gmail.com
# Tel: +52 55 4189 3428
# Metodología: DVP-PRO
# ============================================================================

.PHONY: help install install-dev clean test lint format train predict api dashboard docker-build docker-up monitor docs

# Variables
BOOTSTRAP_PYTHON := $(shell command -v python3 || command -v python)
PYTHON := $(if $(wildcard ./venv/bin/python),./venv/bin/python,$(BOOTSTRAP_PYTHON))
PIP := $(PYTHON) -m pip
VENV := venv
PROJECT_NAME := walmart-demand-forecasting
PORT_API := 8000
PORT_DASHBOARD := 8501
PORT_MLFLOW := 5000

# Colores para output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[1;33m
RED := \033[0;31m
NC := \033[0m # No Color

# ============================================================================
# AYUDA Y DOCUMENTACIÓN
# ============================================================================

help: ## Mostrar este mensaje de ayuda
	@echo "$(BLUE)╔═══════════════════════════════════════════════════════════════╗$(NC)"
	@echo "$(BLUE)║  $(GREEN)Walmart Demand Forecasting - Makefile Commands$(BLUE)       ║$(NC)"
	@echo "$(BLUE)║  $(YELLOW)Ing. Daniel Varela Perez | DVP-PRO Methodology$(BLUE)         ║$(NC)"
	@echo "$(BLUE)╚═══════════════════════════════════════════════════════════════╝$(NC)"
	@echo ""
	@echo "$(GREEN)Comandos disponibles:$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""

# ============================================================================
# INSTALACIÓN Y CONFIGURACIÓN
# ============================================================================

install: ## Instalar proyecto en modo producción
	@echo "$(BLUE)📦 Instalando dependencias de producción...$(NC)"
	$(PIP) install -e .
	@echo "$(GREEN)✅ Instalación completada$(NC)"

install-dev: ## Instalar proyecto en modo desarrollo (con deps dev)
	@echo "$(BLUE)📦 Instalando dependencias de desarrollo...$(NC)"
	$(PIP) install -e ".[dev]"
	@echo "$(GREEN)✅ Instalación de desarrollo completada$(NC)"

install-all: ## Instalar todas las dependencias (prod + dev + mlops)
	@echo "$(BLUE)📦 Instalando todas las dependencias...$(NC)"
	$(PIP) install -e ".[all]"
	@echo "$(GREEN)✅ Instalación completa terminada$(NC)"

venv: ## Crear entorno virtual
	@echo "$(BLUE)🔧 Creando entorno virtual...$(NC)"
	$(BOOTSTRAP_PYTHON) -m venv $(VENV)
	@echo "$(GREEN)✅ Entorno virtual creado en ./$(VENV)$(NC)"
	@echo "$(YELLOW)💡 Activa con: source $(VENV)/bin/activate$(NC)"

# ============================================================================
# LIMPIEZA
# ============================================================================

clean: ## Limpiar archivos temporales y cache
	@echo "$(BLUE)🧹 Limpiando archivos temporales...$(NC)"
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '*.egg-info' -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name '.pytest_cache' -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name '.mypy_cache' -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name 'htmlcov' -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '.coverage' -delete 2>/dev/null || true
	@echo "$(GREEN)✅ Limpieza completada$(NC)"

clean-all: clean ## Limpieza profunda (incluye modelos y logs)
	@echo "$(BLUE)🧹 Limpieza profunda...$(NC)"
	rm -rf logs/*.log 2>/dev/null || true
	rm -rf reports/figures/*.png 2>/dev/null || true
	rm -rf mlruns/ 2>/dev/null || true
	@echo "$(GREEN)✅ Limpieza profunda completada$(NC)"

# ============================================================================
# TESTING Y CALIDAD DE CÓDIGO
# ============================================================================

test: ## Ejecutar tests unitarios
	@echo "$(BLUE)🧪 Ejecutando tests...$(NC)"
	$(PYTHON) -m pytest tests/ -v --cov=src --cov-report=term-missing

test-fast: ## Ejecutar tests sin coverage (rápido)
	@echo "$(BLUE)⚡ Ejecutando tests rápidos...$(NC)"
	$(PYTHON) -m pytest tests/ -v

test-cov: ## Ejecutar tests con reporte HTML de coverage
	@echo "$(BLUE)📊 Generando reporte de cobertura...$(NC)"
	$(PYTHON) -m pytest tests/ -v --cov=src --cov-report=html
	@echo "$(GREEN)✅ Reporte generado en htmlcov/index.html$(NC)"

test-integration: ## Ejecutar solo tests de integración
	@echo "$(BLUE)🔗 Ejecutando tests de integración...$(NC)"
	$(PYTHON) -m pytest tests/ -v -m integration

lint: ## Ejecutar linters (flake8, mypy)
	@echo "$(BLUE)🔍 Ejecutando linters...$(NC)"
	$(PYTHON) -m flake8 src/ --count --select=E9,F63,F7,F82 --show-source --statistics
	$(PYTHON) -m flake8 src/ --count --exit-zero --max-complexity=10 --max-line-length=100
	$(PYTHON) -m mypy src/ --ignore-missing-imports

format: ## Formatear código con black
	@echo "$(BLUE)✨ Formateando código...$(NC)"
	$(PYTHON) -m black src/ tests/
	$(PYTHON) -m isort src/ tests/
	@echo "$(GREEN)✅ Código formateado$(NC)"

check: lint test ## Ejecutar todas las validaciones (lint + test)
	@echo "$(GREEN)✅ Todas las validaciones pasaron$(NC)"

# ============================================================================
# MACHINE LEARNING - ENTRENAMIENTO Y PREDICCIÓN
# ============================================================================

train: ## Entrenar modelo de demand forecasting
	@echo "$(BLUE)🚀 Entrenando modelo de demand forecasting...$(NC)"
	$(PYTHON) -m src.models.train_demand
	@echo "$(GREEN)✅ Entrenamiento completado$(NC)"

predict: ## Realizar predicciones (requiere modelo entrenado)
	@echo "$(BLUE)🔮 Ejecutando predicciones...$(NC)"
	$(PYTHON) -m src.models.predict
	@echo "$(GREEN)✅ Predicciones completadas$(NC)"

evaluate: ## Evaluar modelo en conjunto de validación
	@echo "$(BLUE)📊 Evaluando modelo...$(NC)"
	@latest_pred=$$(ls -t data/predictions/predictions_*.csv | head -n 1); \
	echo "$(YELLOW)Usando predicciones: $$latest_pred$(NC)"; \
	$(PYTHON) -m src.models.evaluate \
		--predictions-path $$latest_pred \
		--actuals-path data/processed/valid_data.csv
	@echo "$(GREEN)✅ Evaluación completada$(NC)"

eda: ## Abrir notebook de EDA
	@echo "$(BLUE)📊 Abriendo notebook de EDA...$(NC)"
	$(PYTHON) -m jupyter notebook notebooks/01_eda.ipynb

notebooks: ## Iniciar Jupyter Lab
	@echo "$(BLUE)📓 Iniciando Jupyter Lab...$(NC)"
	$(PYTHON) -m jupyter lab

# ============================================================================
# API Y SERVICIOS
# ============================================================================

api: ## Iniciar API REST (FastAPI)
	@echo "$(BLUE)🚀 Iniciando API en puerto $(PORT_API)...$(NC)"
	@echo "$(YELLOW)📖 Documentación: http://localhost:$(PORT_API)/docs$(NC)"
	$(PYTHON) -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port $(PORT_API)

api-prod: ## Iniciar API en modo producción
	@echo "$(BLUE)🚀 Iniciando API en modo producción...$(NC)"
	$(PYTHON) -m uvicorn src.api.main:app --host 0.0.0.0 --port $(PORT_API) --workers 4

dashboard: ## Iniciar dashboard de Streamlit
	@echo "$(BLUE)📊 Iniciando dashboard en puerto $(PORT_DASHBOARD)...$(NC)"
	$(PYTHON) -m streamlit run src/visualization/dashboard.py --server.port $(PORT_DASHBOARD)

# ============================================================================
# MLFLOW - TRACKING Y MODEL REGISTRY
# ============================================================================

mlflow-ui: ## Iniciar MLflow UI
	@echo "$(BLUE)📊 Iniciando MLflow UI en http://localhost:$(PORT_MLFLOW)$(NC)"
	$(PYTHON) -m mlflow ui --host 0.0.0.0 --port $(PORT_MLFLOW)

mlflow-server: ## Iniciar MLflow server (tracking server)
	@echo "$(BLUE)🚀 Iniciando MLflow tracking server...$(NC)"
	$(PYTHON) -m mlflow server --host 0.0.0.0 --port $(PORT_MLFLOW) --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns

mlflow-list: ## Listar experimentos de MLflow
	@echo "$(BLUE)📋 Experimentos en MLflow:$(NC)"
	$(PYTHON) -m mlflow experiments list

mlflow-runs: ## Listar runs del experimento
	@echo "$(BLUE)📋 Runs del experimento:$(NC)"
	$(PYTHON) -m mlflow runs list --experiment-name walmart-forecasting

mlflow-clean: ## Limpiar experimentos de MLflow
	@echo "$(YELLOW)⚠️  Limpiando experimentos de MLflow...$(NC)"
	rm -rf mlruns/
	rm -f mlflow.db
	@echo "$(GREEN)✅ MLflow limpiado$(NC)"

# ============================================================================
# MONITOREO
# ============================================================================

monitor: ## Ejecutar monitoreo de drift y performance
	@echo "$(BLUE)📡 Ejecutando monitoreo...$(NC)"
	$(PYTHON) -m src.monitoring.monitoring_run \
		--current-data data/processed/current_data.csv \
		--reference-data data/processed/train_data.csv
	@echo "$(GREEN)✅ Monitoreo completado. Ver: reports/monitoring/$(NC)"

monitor-report: ## Ver último reporte de monitoreo
	@echo "$(BLUE)📄 Abriendo reporte de monitoreo...$(NC)"
	cat reports/monitoring/monitoring_issues.json | python -m json.tool

drift-check: ## Verificar drift en datos de producción
	@echo "$(BLUE)🔍 Verificando drift de datos...$(NC)"
	$(PYTHON) -m src.monitoring.drift_detection
	@echo "$(GREEN)✅ Verificación de drift completada$(NC)"

# ============================================================================
# DOCKER
# ============================================================================

docker-build: ## Construir imagen Docker
	@echo "$(BLUE)🐳 Construyendo imagen Docker...$(NC)"
	docker build -t $(PROJECT_NAME):latest .
	@echo "$(GREEN)✅ Imagen construida: $(PROJECT_NAME):latest$(NC)"

docker-run: ## Ejecutar contenedor Docker
	@echo "$(BLUE)🐳 Ejecutando contenedor...$(NC)"
	docker run -d -p $(PORT_API):$(PORT_API) --name walmart-api $(PROJECT_NAME):latest
	@echo "$(GREEN)✅ Contenedor ejecutándose: http://localhost:$(PORT_API)$(NC)"

docker-stop: ## Detener contenedor Docker
	@echo "$(BLUE)🛑 Deteniendo contenedor...$(NC)"
	docker stop walmart-api || true
	docker rm walmart-api || true
	@echo "$(GREEN)✅ Contenedor detenido$(NC)"

docker-up: ## Levantar todos los servicios con docker-compose
	@echo "$(BLUE)🐳 Levantando servicios con docker-compose...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)✅ Servicios iniciados$(NC)"
	@echo "$(YELLOW)API: http://localhost:$(PORT_API)$(NC)"
	@echo "$(YELLOW)Dashboard: http://localhost:$(PORT_DASHBOARD)$(NC)"
	@echo "$(YELLOW)MLflow: http://localhost:$(PORT_MLFLOW)$(NC)"

docker-down: ## Detener servicios de docker-compose
	@echo "$(BLUE)🛑 Deteniendo servicios...$(NC)"
	docker-compose down
	@echo "$(GREEN)✅ Servicios detenidos$(NC)"

docker-logs: ## Ver logs de docker-compose
	docker-compose logs -f

docker-rebuild: ## Reconstruir y reiniciar servicios
	@echo "$(BLUE)🔄 Reconstruyendo servicios...$(NC)"
	docker-compose down
	docker-compose build --no-cache
	docker-compose up -d
	@echo "$(GREEN)✅ Servicios reconstruidos$(NC)"

# ============================================================================
# DEPLOYMENT
# ============================================================================

deploy-dev: ## Deploy en entorno de desarrollo
	@echo "$(BLUE)🚀 Desplegando en DEV...$(NC)"
	./deployment/deploy.sh dev
	@echo "$(GREEN)✅ Deployment DEV completado$(NC)"

deploy-staging: ## Deploy en entorno de staging
	@echo "$(BLUE)🚀 Desplegando en STAGING...$(NC)"
	./deployment/deploy.sh staging
	@echo "$(GREEN)✅ Deployment STAGING completado$(NC)"

deploy-prod: ## Deploy en entorno de producción
	@echo "$(BLUE)🚀 Desplegando en PRODUCCIÓN...$(NC)"
	./deployment/deploy.sh production
	@echo "$(GREEN)✅ Deployment PRODUCCIÓN completado$(NC)"

# ============================================================================
# DATA PROCESSING
# ============================================================================

download-data: ## Descargar dataset M5 desde Kaggle
	@echo "$(BLUE)📥 Descargando dataset M5...$(NC)"
	kaggle competitions download -c m5-forecasting-accuracy
	unzip m5-forecasting-accuracy.zip -d data/raw/
	@echo "$(GREEN)✅ Dataset descargado$(NC)"

process-data: ## Procesar datos raw
	@echo "$(BLUE)⚙️ Procesando datos...$(NC)"
	$(PYTHON) -m src.data.make_dataset \
		--calendar-path data/raw/calendar.csv \
		--sales-path data/raw/sales_train_validation.csv \
		--prices-path data/raw/sell_prices.csv \
		--output-path data/processed/dataset.parquet
	@echo "$(GREEN)✅ Datos procesados$(NC)"

features: ## Generar features
	@echo "$(BLUE)🔧 Generando features...$(NC)"
	$(PYTHON) -m src.features.build_features
	@echo "$(GREEN)✅ Features generadas$(NC)"

# ============================================================================
# DOCUMENTACIÓN
# ============================================================================

docs: ## Generar documentación del proyecto
	@echo "$(BLUE)📚 Generando documentación...$(NC)"
	@echo "$(YELLOW)Documentos disponibles:$(NC)"
	@ls -lh docs/*.md
	@echo "$(GREEN)✅ Documentación disponible en docs/$(NC)"

readme: ## Abrir README principal
	@less README_FINAL.md

audit: ## Mostrar auditoría DVP-PRO
	@less AUDITORIA_DVP_PRO.md

# ============================================================================
# GIT
# ============================================================================

git-status: ## Ver estado del repositorio
	@git status

git-log: ## Ver historial de commits
	@git log --oneline --graph --all -10

commit: ## Commit rápido (use: make commit m="mensaje")
	@if [ -z "$(m)" ]; then \
		echo "$(RED)❌ Error: Especifica mensaje con m=\"mensaje\"$(NC)"; \
		exit 1; \
	fi
	git add .
	git commit -m "$(m)"
	@echo "$(GREEN)✅ Commit realizado$(NC)"

# ============================================================================
# UTILIDADES
# ============================================================================

info: ## Mostrar información del proyecto
	@echo "$(BLUE)╔═══════════════════════════════════════════════════════════════╗$(NC)"
	@echo "$(BLUE)║  $(GREEN)Walmart Demand Forecasting - Project Info$(BLUE)            ║$(NC)"
	@echo "$(BLUE)╚═══════════════════════════════════════════════════════════════╝$(NC)"
	@echo ""
	@echo "$(YELLOW)Proyecto:$(NC)     $(PROJECT_NAME)"
	@echo "$(YELLOW)Versión:$(NC)      1.2.0"
	@echo "$(YELLOW)Python:$(NC)       $$($(PYTHON) --version)"
	@echo "$(YELLOW)Autor:$(NC)        Ing. Daniel Varela Perez"
	@echo "$(YELLOW)Email:$(NC)        bedaniele0@gmail.com"
	@echo "$(YELLOW)Metodología:$(NC)  DVP-PRO"
	@echo ""
	@echo "$(YELLOW)Dataset:$(NC)      M5 Forecasting (Walmart)"
	@echo "$(YELLOW)Series:$(NC)       30,490 product-store combinations"
	@echo "$(YELLOW)Período:$(NC)      2011-2016 (5.4 años)"
	@echo ""

setup: venv install-dev ## Setup completo inicial (venv + install-dev)
	@echo "$(GREEN)✅ Setup inicial completado$(NC)"
	@echo "$(YELLOW)💡 Activa el entorno: source $(VENV)/bin/activate$(NC)"

pipeline: process-data features train evaluate ## Ejecutar pipeline completo
	@echo "$(GREEN)✅ Pipeline completo ejecutado$(NC)"

# Default target
.DEFAULT_GOAL := help
