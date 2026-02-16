#!/bin/bash
# Run API locally without Docker
# Author: Ing. Daniel Varela Perez
# Date: December 5, 2024

echo "=============================================="
echo " Starting Walmart Forecasting API (Local)"
echo "=============================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found"
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies if needed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install fastapi uvicorn pydantic joblib numpy pandas lightgbm
fi

# Check if model exists
if [ ! -f "models/lightgbm_model.pkl" ]; then
    echo "❌ Model file not found: models/lightgbm_model.pkl"
    exit 1
fi

echo ""
echo "✅ Starting API on http://localhost:8000"
echo ""
echo "Endpoints:"
echo "  - Health: http://localhost:8000/health"
echo "  - Docs: http://localhost:8000/docs"
echo "  - Model Info: http://localhost:8000/model/info"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Run API
uvicorn src.api.main:app --host 0.0.0.0 --port 8000
