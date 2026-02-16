# ============================================================================
# Makefile - Fraud Detection System Project Automation
# ============================================================================
# Comandos automatizados para desarrollo, testing, deployment y operación
#
# Autor: Ing. Daniel Varela Perez
# Email: bedaniele0@gmail.com
# Tel: +52 55 4189 3428
# Metodología: DVP-PRO
# ============================================================================

.PHONY: help install install-dev install-all venv clean clean-pyc clean-test
.PHONY: lint format check typecheck test test-fast test-cov test-integration
.PHONY: train predict evaluate dashboard api mlflow-ui monitor
.PHONY: docker-build docker-up docker-down docker-logs docker-rebuild
.PHONY: deploy-dev deploy-staging deploy-prod
.PHONY: download-data process-data eda notebooks info setup pipeline

# Variables
PYTHON := python3
PIP := $(PYTHON) -m pip
PYTEST := $(PYTHON) -m pytest
BLACK := $(PYTHON) -m black
RUFF := $(PYTHON) -m ruff
MYPY := $(PYTHON) -m mypy
UVICORN := $(PYTHON) -m uvicorn
STREAMLIT := $(PYTHON) -m streamlit

PROJECT_NAME := fraud-detection-system
SRC_DIR := src
TEST_DIR := tests
DATA_DIR := data
MODELS_DIR := models
REPORTS_DIR := reports
DASHBOARD_DIR := dashboard

# Colors
BLUE := \\033[0;34m
GREEN := \\033[0;32m
RED := \\033[0;31m
NC := \\033[0m # No Color

# ============================================================================
# HELP
# ============================================================================

help: ## Muestra este mensaje de ayuda
	@echo "$(BLUE)═══════════════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)  Fraud Detection System - Makefile Commands$(NC)"
	@echo "$(GREEN)  Metodología DVP-PRO$(NC)"
	@echo "$(BLUE)═══════════════════════════════════════════════════════════════$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(BLUE)%-20s$(NC) %s\\n", $$1, $$2}'
	@echo ""
	@echo "$(BLUE)═══════════════════════════════════════════════════════════════$(NC)"

# ============================================================================
# SETUP & INSTALLATION
# ============================================================================

venv: ## Crear entorno virtual
	@echo "$(GREEN)Creating virtual environment...$(NC)"
	$(PYTHON) -m venv venv_fraud
	@echo "$(GREEN)✓ Virtual environment created$(NC)"
	@echo "Activate with: source venv_fraud/bin/activate"

install: ## Instalar dependencias básicas
	@echo "$(GREEN)Installing dependencies...$(NC)"
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -r requirements.txt
	$(PIP) install -e .
	@echo "$(GREEN)✓ Dependencies installed$(NC)"

install-dev: ## Instalar dependencias de desarrollo
	@echo "$(GREEN)Installing dev dependencies...$(NC)"
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -r requirements.txt
	$(PIP) install -e ".[dev]"
	@echo "$(GREEN)✓ Dev dependencies installed$(NC)"

install-all: ## Instalar todas las dependencias
	@echo "$(GREEN)Installing all dependencies...$(NC)"
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -r requirements.txt
	$(PIP) install -e ".[all]"
	@echo "$(GREEN)✓ All dependencies installed$(NC)"

setup: install ## Setup completo del proyecto
	@echo "$(GREEN)Setting up project...$(NC)"
	mkdir -p logs data/raw data/processed data/predictions
	mkdir -p models reports/figures reports/metrics reports/monitoring
	mkdir -p api/routers
	@echo "$(GREEN)✓ Project setup complete$(NC)"

verify: ## Verificar configuración completa
	@echo "$(GREEN)Verifying setup...$(NC)"
	$(PYTHON) scripts/verify_setup_complete.py

# ============================================================================
# CODE QUALITY
# ============================================================================

lint: ## Ejecutar linting con Ruff
	@echo "$(GREEN)Running Ruff linter...$(NC)"
	$(RUFF) check $(SRC_DIR) $(TEST_DIR) $(DASHBOARD_DIR)

format: ## Formatear código con Black
	@echo "$(GREEN)Formatting code with Black...$(NC)"
	$(BLACK) $(SRC_DIR) $(TEST_DIR) $(DASHBOARD_DIR)

check: lint ## Verificar código (lint + format check)
	@echo "$(GREEN)Checking code formatting...$(NC)"
	$(BLACK) --check $(SRC_DIR) $(TEST_DIR) $(DASHBOARD_DIR)

typecheck: ## Verificar tipos con MyPy
	@echo "$(GREEN)Type checking with MyPy...$(NC)"
	$(MYPY) $(SRC_DIR) --ignore-missing-imports

# ============================================================================
# TESTING
# ============================================================================

test: ## Ejecutar tests
	@echo "$(GREEN)Running tests...$(NC)"
	$(PYTEST) $(TEST_DIR) -v

test-fast: ## Ejecutar tests rápidos (sin slow)
	@echo "$(GREEN)Running fast tests...$(NC)"
	$(PYTEST) $(TEST_DIR) -v -m "not slow"

test-cov: ## Ejecutar tests con coverage
	@echo "$(GREEN)Running tests with coverage...$(NC)"
	$(PYTEST) $(TEST_DIR) -v --cov=$(SRC_DIR) --cov-report=term-missing --cov-report=html

test-integration: ## Ejecutar tests de integración
	@echo "$(GREEN)Running integration tests...$(NC)"
	$(PYTEST) $(TEST_DIR) -v -m integration

test-api: ## Ejecutar tests de API
	@echo "$(GREEN)Running API tests...$(NC)"
	$(PYTEST) $(TEST_DIR) -v -m api

test-dashboard: ## Ejecutar tests de dashboard
	@echo "$(GREEN)Running dashboard tests...$(NC)"
	$(PYTEST) $(TEST_DIR) -v -m dashboard

# ============================================================================
# TRAINING & MODELING
# ============================================================================

train: ## Entrenar modelo de fraud detection
	@echo "$(GREEN)Training fraud detection model...$(NC)"
	$(PYTHON) -m src.models.train_fraud \
		--train-path $(DATA_DIR)/processed/train_clean.parquet/part.0.parquet \
		--val-path $(DATA_DIR)/processed/validation_clean.parquet

predict: ## Generar predicciones
	@echo "$(GREEN)Generating predictions...$(NC)"
	$(PYTHON) -m src.models.predict --input-path $(DATA_DIR)/processed/test_clean.parquet --output-path reports/predictions/predicciones.csv

evaluate: ## Evaluar modelo
	@echo "$(GREEN)Evaluating model...$(NC)"
	$(PYTHON) -m src.models.evaluate \
		--test-path $(DATA_DIR)/processed/test_clean.parquet

# ============================================================================
# SERVICES
# ============================================================================

dashboard: ## Iniciar dashboard Streamlit
	@echo "$(GREEN)Starting Streamlit dashboard...$(NC)"
	$(STREAMLIT) run $(DASHBOARD_DIR)/fraud_detection_dashboard.py --server.port 8501

api: ## Iniciar API (development)
	@echo "$(GREEN)Starting API server (development)...$(NC)"
	$(UVICORN) api.main:app --reload --host 0.0.0.0 --port 8000

api-prod: ## Iniciar API (production)
	@echo "$(GREEN)Starting API server (production)...$(NC)"
	$(UVICORN) api.main:app --host 0.0.0.0 --port 8000 --workers 4

mlflow-ui: ## Iniciar MLflow UI
	@echo "$(GREEN)Starting MLflow UI...$(NC)"
	mlflow ui --host 0.0.0.0 --port 5000

mlflow-server: ## Iniciar MLflow tracking server
	@echo "$(GREEN)Starting MLflow tracking server...$(NC)"
	mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns --host 0.0.0.0 --port 5000

monitor: ## Ejecutar monitoring
	@echo "$(GREEN)Running monitoring...$(NC)"
	$(PYTHON) -m src.monitoring.monitoring_run

# ============================================================================
# MLFLOW
# ============================================================================

mlflow-list: ## Listar experimentos MLflow
	@echo "$(GREEN)Listing MLflow experiments...$(NC)"
	mlflow experiments list

mlflow-runs: ## Listar runs de MLflow
	@echo "$(GREEN)Listing MLflow runs...$(NC)"
	mlflow runs list --experiment-name fraud-detection

mlflow-clean: ## Limpiar runs antiguos
	@echo "$(RED)Cleaning old MLflow runs...$(NC)"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		rm -rf mlruns/ mlflow.db; \
		echo "\\n$(GREEN)✓ MLflow data cleaned$(NC)"; \
	fi

# ============================================================================
# DOCKER
# ============================================================================

docker-build: ## Build Docker image
	@echo "$(GREEN)Building Docker image...$(NC)"
	docker build -t fraud-detection-api:latest .

docker-up: ## Iniciar servicios Docker
	@echo "$(GREEN)Starting Docker services...$(NC)"
	docker-compose up -d

docker-down: ## Detener servicios Docker
	@echo "$(GREEN)Stopping Docker services...$(NC)"
	docker-compose down

docker-logs: ## Ver logs de Docker
	docker-compose logs -f

docker-rebuild: docker-down docker-build docker-up ## Rebuild y restart Docker

docker-shell: ## Shell en contenedor Docker
	docker-compose exec api /bin/bash

# ============================================================================
# DEPLOYMENT
# ============================================================================

deploy-dev: ## Deploy a desarrollo
	@echo "$(GREEN)Deploying to development...$(NC)"
	./deployment/deploy.sh dev

deploy-staging: ## Deploy a staging
	@echo "$(GREEN)Deploying to staging...$(NC)"
	./deployment/deploy.sh staging

deploy-prod: ## Deploy a producción
	@echo "$(RED)Deploying to production...$(NC)"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		./deployment/deploy.sh production; \
	fi

# ============================================================================
# DATA
# ============================================================================

download-data: ## Descargar dataset
	@echo "$(GREEN)Downloading fraud detection dataset...$(NC)"
	@echo "$(BLUE)Dataset should be placed in data/raw/$(NC)"

process-data: ## Procesar datos
	@echo "$(GREEN)Processing data...$(NC)"
	$(PYTHON) $(DATA_DIR)/processed/load_clean_pipeline.py

eda: ## Abrir notebook de EDA
	@echo "$(GREEN)Opening EDA notebook...$(NC)"
	jupyter notebook notebooks/01_fraud_eda.ipynb

notebooks: ## Iniciar Jupyter Lab
	@echo "$(GREEN)Starting Jupyter Lab...$(NC)"
	jupyter lab

# ============================================================================
# CLEANING
# ============================================================================

clean: clean-pyc clean-test ## Limpiar archivos temporales

clean-pyc: ## Limpiar archivos Python cache
	@echo "$(GREEN)Cleaning Python cache files...$(NC)"
	find . -type f -name '*.py[co]' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '.pytest_cache' -delete
	find . -type d -name '.mypy_cache' -delete
	find . -type d -name '.ruff_cache' -delete
	find . -type f -name '.DS_Store' -delete

clean-test: ## Limpiar archivos de tests
	@echo "$(GREEN)Cleaning test files...$(NC)"
	rm -rf .coverage htmlcov/ .pytest_cache/
	find . -type f -name '.coverage.*' -delete

clean-all: clean ## Limpiar todo (incluye venv)
	@echo "$(RED)Cleaning everything...$(NC)"
	rm -rf venv_fraud/
	rm -rf build/ dist/ *.egg-info

# ============================================================================
# UTILS
# ============================================================================

info: ## Mostrar información del proyecto
	@echo "$(BLUE)═══════════════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)  Fraud Detection System - Project Info$(NC)"
	@echo "$(BLUE)═══════════════════════════════════════════════════════════════$(NC)"
	@echo "Project:        $(PROJECT_NAME)"
	@echo "Version:        1.0.0"
	@echo "Author:         Ing. Daniel Varela Perez"
	@echo "Email:          bedaniele0@gmail.com"
	@echo "Methodology:    DVP-PRO"
	@echo ""
	@echo "Python:         $$($(PYTHON) --version)"
	@echo "Pip:            $$($(PIP) --version | cut -d' ' -f2)"
	@echo ""
	@echo "Directories:"
	@echo "  Source:       $(SRC_DIR)"
	@echo "  Tests:        $(TEST_DIR)"
	@echo "  Data:         $(DATA_DIR)"
	@echo "  Models:       $(MODELS_DIR)"
	@echo "  Reports:      $(REPORTS_DIR)"
	@echo "  Dashboard:    $(DASHBOARD_DIR)"
	@echo "$(BLUE)═══════════════════════════════════════════════════════════════$(NC)"

pipeline: process-data train predict evaluate ## Ejecutar pipeline completo
	@echo "$(GREEN)✓ Pipeline completed successfully!$(NC)"

run-all: dashboard ## Alias para iniciar dashboard
	@echo "$(GREEN)Dashboard running on http://localhost:8501$(NC)"

list: ## Listar todos los comandos disponibles
	@echo "$(GREEN)Available commands:$(NC)"
	@$(MAKE) -qp | awk -F':' '/^[a-zA-Z0-9][^$$#\/\t=]*:([^=]|$$)/ {split($$1,A,/ /);for(i in A)print A[i]}' | grep -v '__' | sort

# ============================================================================
# QUICK START
# ============================================================================

quickstart: install setup verify dashboard ## Setup rápido y lanzar dashboard
	@echo "$(GREEN)✓ Quickstart complete!$(NC)"

# ============================================================================
# STATUS
# ============================================================================

status: ## Estado del proyecto
	@echo "$(BLUE)Project Status:$(NC)"
	@echo "  Git branch: $$(git branch --show-current 2>/dev/null || echo 'N/A')"
	@echo "  Git status: $$(git status -s 2>/dev/null | wc -l) files changed"
	@echo "  Python:     $$($(PYTHON) --version)"
	@echo "  Tests:      $$(find $(TEST_DIR) -name 'test_*.py' | wc -l) test files"
	@echo "  Models:     $$(find $(MODELS_DIR) -name '*.pkl' | wc -l) model files"
