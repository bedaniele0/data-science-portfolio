PY ?= python3
VENV ?= .venv

.PHONY: install setup train score monitor test

setup:
	$(PY) -m venv $(VENV)
	$(VENV)/bin/pip install -r requirements.txt

install: setup

train:
	STORAGE_MODE=local $(PY) src/train_model.py

score:
	STORAGE_MODE=local $(PY) src/batch_scoring.py

monitor:
	STORAGE_MODE=local $(PY) src/monitor_data_drift.py
	STORAGE_MODE=local $(PY) src/monitor_performance.py

test:
	$(PY) -m pytest -q
