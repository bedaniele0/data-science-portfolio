.PHONY: help ingest relevance clustering master serving dashboard-contract test validate-artifacts validate-notebooks validate notebooks api dashboard run

help:
	@echo "Available targets:"
	@echo "  make ingest              Run ingestion pipeline"
	@echo "  make relevance           Run ingestion + relevance baseline"
	@echo "  make clustering          Run ingestion + relevance + clustering"
	@echo "  make master              Build SQLite master database"
	@echo "  make serving             Validate serving/API query contract"
	@echo "  make dashboard-contract  Validate dashboard data contract"
	@echo "  make test                Run unit and integration tests"
	@echo "  make validate-artifacts  Check required artifacts and report schemas"
	@echo "  make validate-notebooks  Execute notebooks with nbmake"
	@echo "  make validate            Run full E2E validation gate"
	@echo "  make notebooks           Open JupyterLab"
	@echo "  make api                 Open FastAPI on http://127.0.0.1:8000"
	@echo "  make dashboard           Open Streamlit on http://127.0.0.1:8501"

ingest:
	uv run python -m src.pipelines.ingest_pipeline --config configs/ingestion.yaml

relevance: ingest
	uv run python -m src.pipelines.relevance_pipeline --config configs/relevance.yaml

clustering: relevance
	uv run python -m src.pipelines.clustering_pipeline --config configs/clustering.yaml

master: clustering
	uv run python -m src.pipelines.build_master_pipeline --config configs/storage.yaml

serving: master
	uv run python -m src.pipelines.serving_contract_pipeline --config configs/serving.yaml

dashboard-contract: serving
	uv run python -m src.pipelines.dashboard_contract_pipeline --config configs/dashboard.yaml

test:
	uv run --extra dashboard pytest

validate-artifacts:
	uv run python scripts/validate_artifacts.py

validate-notebooks:
	uv run --extra validation pytest --nbmake notebooks

validate: dashboard-contract test validate-artifacts validate-notebooks

notebooks:
	uv run --extra notebooks jupyter lab notebooks

api: master
	uv run uvicorn src.serving.api:app --reload --host 127.0.0.1 --port 8000

dashboard: dashboard-contract
	uv run --extra dashboard streamlit run src/dashboard/app.py

run: validate
