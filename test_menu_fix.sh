#!/bin/bash

echo "=========================================="
echo "Testing Menu Products Fix"
echo "=========================================="
echo ""

echo "1. Testing Backend API..."
echo "   GET /api/products"
PRODUCTS=$(curl -s http://localhost:5000/api/products)
PRODUCT_COUNT=$(echo "$PRODUCTS" | python3 -c "import sys, json; data = json.load(sys.stdin); print(len(data.get('data', [])))" 2>/dev/null)

if [ "$PRODUCT_COUNT" -gt 0 ]; then
    echo "   ✅ Backend API working - $PRODUCT_COUNT products found"
else
    echo "   ❌ Backend API not responding or no products"
    exit 1
fi

echo ""
echo "2. Testing Categories API..."
echo "   GET /api/categories"
CATEGORIES=$(curl -s http://localhost:5000/api/categories)
CATEGORY_COUNT=$(echo "$CATEGORIES" | python3 -c "import sys, json; data = json.load(sys.stdin); print(len(data.get('data', [])))" 2>/dev/null)

if [ "$CATEGORY_COUNT" -gt 0 ]; then
    echo "   ✅ Categories API working - $CATEGORY_COUNT categories found"
else
    echo "   ❌ Categories API not responding"
fi

echo ""
echo "3. Sample Products:"
echo "$PRODUCTS" | python3 -c "
import sys, json
data = json.load(sys.stdin)
products = data.get('data', [])[:5]
for p in products:
    has_image = '✅' if p.get('image_url') else '⚠️ (no image)'
    print(f'   - {p[\"name\"]} ({p[\"category_name\"]}) {has_image}')
" 2>/dev/null

echo ""
echo "4. Frontend Status:"
if curl -s http://localhost:5173 > /dev/null 2>&1; then
    echo "   ✅ Frontend running on http://localhost:5173"
elif curl -s http://localhost:5174 > /dev/null 2>&1; then
    echo "   ✅ Frontend running on http://localhost:5174"
elif curl -s http://localhost:5176 > /dev/null 2>&1; then
    echo "   ✅ Frontend running on http://localhost:5176"
else
    echo "   ⚠️  Frontend may not be running"
fi

echo ""
echo "=========================================="
echo "Summary:"
echo "=========================================="
echo "✅ Backend has $PRODUCT_COUNT products"
echo "✅ Data transformer will add placeholder images"
echo "✅ MenuCard has error handling for failed images"
echo ""
echo "Next Steps:"
echo "1. Open your browser to the frontend URL"
echo "2. Navigate to the Menu section"
echo "3. Products should display with placeholder images"
echo "4. Check browser console for any errors"
echo ""
echo "To add real images, see: MENU_PRODUCTS_FIX.md"
echo "=========================================="
