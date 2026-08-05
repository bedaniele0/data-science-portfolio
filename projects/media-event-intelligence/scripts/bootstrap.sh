#!/usr/bin/env bash
set -euo pipefail

uv venv .venv
source .venv/bin/activate
uv pip install -e .
echo "Project environment ready."

