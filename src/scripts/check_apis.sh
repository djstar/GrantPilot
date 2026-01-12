#!/bin/bash
# GrantPilot API Health Check Script
# Run this to verify all services are working

set -e

API_URL="${API_URL:-http://localhost:8000}"
FRONTEND_URL="${FRONTEND_URL:-http://localhost:5173}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo ""
echo "=========================================="
echo "  GrantPilot API Health Check"
echo "=========================================="
echo ""

# Helper function to check endpoint
check_endpoint() {
    local name="$1"
    local url="$2"
    local expected_field="$3"

    printf "%-30s" "$name..."

    http_code=$(curl -s -o /tmp/grantpilot_check.json -w "%{http_code}" "$url" 2>/dev/null)
    body=$(cat /tmp/grantpilot_check.json 2>/dev/null)

    if [ "$http_code" == "200" ]; then
        if [ -n "$expected_field" ]; then
            if echo "$body" | grep -q "$expected_field"; then
                echo -e "${GREEN}✓ OK${NC}"
                return 0
            else
                echo -e "${YELLOW}⚠ Unexpected response${NC}"
                return 1
            fi
        else
            echo -e "${GREEN}✓ OK${NC}"
            return 0
        fi
    else
        echo -e "${RED}✗ Failed (HTTP $http_code)${NC}"
        return 1
    fi
}

# Check core services
echo -e "${BLUE}Core Services:${NC}"
echo "-------------------------------------------"

check_endpoint "API Root" "$API_URL/" "running"
check_endpoint "Health Check" "$API_URL/health" "healthy"
check_endpoint "Database" "$API_URL/health/db" "connected"
check_endpoint "Redis" "$API_URL/health/redis" "connected"
check_endpoint "Full Health" "$API_URL/health/full" "services"

echo ""
echo -e "${BLUE}API Endpoints:${NC}"
echo "-------------------------------------------"

check_endpoint "Projects List" "$API_URL/api/projects" "items"
check_endpoint "Documents List" "$API_URL/api/documents" "items"

echo ""
echo -e "${BLUE}LLM Services:${NC}"
echo "-------------------------------------------"

check_endpoint "Embeddings Status" "$API_URL/health/embeddings" "status"
check_endpoint "LLM Status" "$API_URL/health/llm" "status"

echo ""
echo -e "${BLUE}Frontend:${NC}"
echo "-------------------------------------------"

printf "%-30s" "Frontend Server..."
if curl -s "$FRONTEND_URL" | grep -q "GrantPilot" 2>/dev/null; then
    echo -e "${GREEN}✓ OK${NC}"
else
    echo -e "${RED}✗ Not responding${NC}"
fi

echo ""
echo "=========================================="

# Get full health status
echo ""
echo -e "${BLUE}Detailed Status:${NC}"
echo "-------------------------------------------"
curl -s "$API_URL/health/full" | python3 -m json.tool 2>/dev/null || echo "Could not parse response"

echo ""
echo "=========================================="
echo ""

# Summary
full_status=$(curl -s "$API_URL/health/full" 2>/dev/null)
overall=$(echo "$full_status" | python3 -c "import sys, json; print(json.load(sys.stdin).get('status', 'unknown'))" 2>/dev/null)

if [ "$overall" == "healthy" ]; then
    echo -e "${GREEN}✓ All services healthy!${NC}"
elif [ "$overall" == "degraded" ]; then
    echo -e "${YELLOW}⚠ Some services unconfigured (check API keys)${NC}"
else
    echo -e "${RED}✗ Some services unhealthy${NC}"
fi

echo ""
echo "API Docs: $API_URL/docs"
echo "Frontend: $FRONTEND_URL"
echo ""
