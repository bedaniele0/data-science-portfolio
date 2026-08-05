FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1     UV_SYSTEM_PYTHON=1

WORKDIR /app

RUN apt-get update     && apt-get install -y --no-install-recommends curl make     && rm -rf /var/lib/apt/lists/*     && pip install --no-cache-dir uv==0.11.6

COPY . .
RUN uv sync --frozen --extra dashboard --extra validation     && make dashboard-contract

FROM base AS api
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3     CMD curl --fail --silent http://127.0.0.1:8000/health || exit 1
CMD ["uv", "run", "uvicorn", "src.serving.api:app", "--host", "0.0.0.0", "--port", "8000"]

FROM base AS dashboard
EXPOSE 8501
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3     CMD curl --fail --silent http://127.0.0.1:8501/_stcore/health || exit 1
CMD ["uv", "run", "--extra", "dashboard", "streamlit", "run", "src/dashboard/app.py", "--server.address=0.0.0.0", "--server.port=8501"]
