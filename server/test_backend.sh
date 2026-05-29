#!/bin/bash
# Quick Backend Test Script

echo "🧪 Testing Driftwood Cafe Backend..."
echo ""

BASE_URL="http://localhost:5000/api"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
PASSED=0
FAILED=0

# Function to test endpoint
test_endpoint() {
    local method=$1
    local endpoint=$2
    local description=$3
    local expected_status=$4
    local data=$5
    local headers=$6
    
    echo -n "Testing: $description... "
    
    if [ "$method" = "GET" ]; then
        response=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL$endpoint" $headers)
    elif [ "$method" = "POST" ]; then
        response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL$endpoint" \
            -H "Content-Type: application/json" \
            -d "$data" $headers)
    fi
    
    status_code=$(echo "$response" | tail -n1)
    
    if [ "$status_code" = "$expected_status" ]; then
        echo -e "${GREEN}✓ PASS${NC} (Status: $status_code)"
        ((PASSED++))
    else
        echo -e "${RED}✗ FAIL${NC} (Expected: $expected_status, Got: $status_code)"
        ((FAILED++))
    fi
}

echo "=== Health Check ==="
test_endpoint "GET" "/health" "Health check" "200"
echo ""

echo "=== Product Endpoints ==="
test_endpoint "GET" "/products" "Get all products" "200"
test_endpoint "GET" "/products/1" "Get product by ID" "200"
test_endpoint "GET" "/products/featured" "Get featured products" "200"
echo ""

echo "=== Category Endpoints ==="
test_endpoint "GET" "/categories" "Get all categories" "200"
test_endpoint "GET" "/categories/1" "Get category by ID" "200"
echo ""

echo "=== Authentication Endpoints ==="
test_endpoint "POST" "/auth/login" "Login with valid credentials" "200" \
    '{"email":"admin@driftwood.com","password":"password123"}'
echo ""

echo "=== Guest Checkout ==="
test_endpoint "POST" "/orders" "Create order (guest)" "201" \
    '{"items":[{"product_id":1,"quantity":2}],"order_type":"pickup","payment_method":"cash"}'
echo ""

echo "================================"
echo -e "Results: ${GREEN}$PASSED passed${NC}, ${RED}$FAILED failed${NC}"
echo "================================"

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}❌ Some tests failed${NC}"
    exit 1
fi
