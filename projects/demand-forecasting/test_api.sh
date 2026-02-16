#!/bin/bash
# Quick API Test Script
# Author: Ing. Daniel Varela Perez
# Date: December 5, 2024

API_URL="http://localhost:8000"

echo "=============================================="
echo " Walmart Forecasting API - Quick Test"
echo "=============================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test function
test_endpoint() {
    local name=$1
    local method=$2
    local endpoint=$3
    local data=$4

    echo -e "${YELLOW}Testing: $name${NC}"

    if [ "$method" = "GET" ]; then
        response=$(curl -s -w "\n%{http_code}" "$API_URL$endpoint")
    else
        response=$(curl -s -w "\n%{http_code}" -X POST "$API_URL$endpoint" \
            -H "Content-Type: application/json" \
            -d "$data")
    fi

    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')

    if [ "$http_code" = "200" ]; then
        echo -e "${GREEN}✅ PASS${NC} (HTTP $http_code)"
        echo "$body" | python3 -m json.tool 2>/dev/null | head -20
    else
        echo -e "${RED}❌ FAIL${NC} (HTTP $http_code)"
        echo "$body"
    fi
    echo ""
}

# Wait for API to be ready
echo "Waiting for API to be ready..."
for i in {1..30}; do
    if curl -s "$API_URL/health" > /dev/null 2>&1; then
        echo -e "${GREEN}API is ready!${NC}"
        break
    fi
    echo -n "."
    sleep 1
done
echo ""

# Run tests
echo "=============================================="
echo " Running Tests"
echo "=============================================="
echo ""

# Test 1: Health Check
test_endpoint "Health Check" "GET" "/health"

# Test 2: Root
test_endpoint "Root Endpoint" "GET" "/"

# Test 3: Model Info
test_endpoint "Model Info" "GET" "/model/info"

# Test 4: Single Prediction
test_endpoint "Single Prediction" "POST" "/predict" \
    '{"item_id": "FOODS_1_001_CA_1", "store_id": "CA_1", "date": "2016-05-01"}'

# Test 5: Batch Prediction
test_endpoint "Batch Prediction" "POST" "/predict/batch" \
    '{"items": [{"item_id": "FOODS_1_001_CA_1", "store_id": "CA_1", "date": "2016-05-01"}]}'

# Test 6: Feature Importance
test_endpoint "Feature Importance" "GET" "/model/features/importance?top_n=5"

echo "=============================================="
echo " Test Summary"
echo "=============================================="
echo "API URL: $API_URL"
echo "Interactive Docs: $API_URL/docs"
echo ""
echo "To see full logs:"
echo "  docker-compose logs -f"
echo ""
echo "To stop API:"
echo "  docker-compose down"
echo ""
