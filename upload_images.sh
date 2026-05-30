#!/bin/bash

# Driftwood Café - Image Upload Helper Script
# This script helps you upload images to products easily

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
API_URL="http://localhost:5000"
CLIENT_ASSETS="client/src/assets"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Driftwood Café - Image Upload Tool${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Step 1: Login
echo -e "${YELLOW}Step 1: Login${NC}"
echo "Enter your admin credentials:"
read -p "Email [admin@driftwood.com]: " EMAIL
EMAIL=${EMAIL:-admin@driftwood.com}

read -sp "Password [admin123]: " PASSWORD
PASSWORD=${PASSWORD:-admin123}
echo ""

echo "Logging in..."
LOGIN_RESPONSE=$(curl -s -X POST "$API_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$EMAIL\",\"password\":\"$PASSWORD\"}")

# Check if login was successful
if echo "$LOGIN_RESPONSE" | grep -q '"success":true'; then
    TOKEN=$(echo "$LOGIN_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])" 2>/dev/null)
    echo -e "${GREEN}✅ Login successful!${NC}"
    echo ""
else
    echo -e "${RED}❌ Login failed!${NC}"
    echo "Response: $LOGIN_RESPONSE"
    echo ""
    echo "Please check your credentials or create an admin account:"
    echo "curl -X POST $API_URL/api/auth/register \\"
    echo "  -H 'Content-Type: application/json' \\"
    echo "  -d '{\"email\":\"admin@driftwood.com\",\"password\":\"admin123\",\"full_name\":\"Admin\",\"phone\":\"+254700000000\",\"role\":\"admin\"}'"
    exit 1
fi

# Step 2: Choose upload mode
echo -e "${YELLOW}Step 2: Choose Upload Mode${NC}"
echo "1) Upload all images automatically (recommended)"
echo "2) Upload images one by one (manual)"
echo "3) Upload a single image to a specific product"
read -p "Choose option [1]: " MODE
MODE=${MODE:-1}
echo ""

# Function to upload image
upload_image() {
    local IMAGE_PATH=$1
    local PRODUCT_ID=$2
    local PRODUCT_NAME=$3
    
    if [ ! -f "$IMAGE_PATH" ]; then
        echo -e "${RED}  ❌ File not found: $IMAGE_PATH${NC}"
        return 1
    fi
    
    echo -e "${BLUE}  Uploading: $PRODUCT_NAME (ID: $PRODUCT_ID)${NC}"
    
    RESPONSE=$(curl -s -X POST "$API_URL/api/upload/product-image" \
      -H "Authorization: Bearer $TOKEN" \
      -F "file=@$IMAGE_PATH" \
      -F "product_id=$PRODUCT_ID" \
      -F "optimize=true" \
      -F "create_thumbnails=true")
    
    if echo "$RESPONSE" | grep -q '"success":true'; then
        IMAGE_URL=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['url'])" 2>/dev/null)
        echo -e "${GREEN}  ✅ Success! Image URL: $IMAGE_URL${NC}"
        return 0
    else
        ERROR=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('error', 'Unknown error'))" 2>/dev/null)
        echo -e "${RED}  ❌ Failed: $ERROR${NC}"
        return 1
    fi
}

# Mode 1: Automatic upload
if [ "$MODE" == "1" ]; then
    echo -e "${YELLOW}Uploading all images automatically...${NC}"
    echo ""
    
    SUCCESS=0
    FAILED=0
    
    # Hot Coffee
    echo -e "${BLUE}Hot Coffee:${NC}"
    upload_image "$CLIENT_ASSETS/Hot_Cold/Hot1.jpg" 1 "Espresso" && ((SUCCESS++)) || ((FAILED++))
    upload_image "$CLIENT_ASSETS/Hot_Cold/Hot2.jpg" 2 "Americano" && ((SUCCESS++)) || ((FAILED++))
    upload_image "$CLIENT_ASSETS/Hot_Cold/Hot3.jpg" 3 "Cappuccino" && ((SUCCESS++)) || ((FAILED++))
    upload_image "$CLIENT_ASSETS/Hot_Cold/Hot1.jpg" 4 "Latte" && ((SUCCESS++)) || ((FAILED++))
    upload_image "$CLIENT_ASSETS/Hot_Cold/Hot2.jpg" 5 "Mocha" && ((SUCCESS++)) || ((FAILED++))
    echo ""
    
    # Cold Coffee
    echo -e "${BLUE}Cold Coffee:${NC}"
    upload_image "$CLIENT_ASSETS/Hot_Cold/Cold1.jpg" 6 "Iced Americano" && ((SUCCESS++)) || ((FAILED++))
    upload_image "$CLIENT_ASSETS/Hot_Cold/Cold2.jpg" 7 "Iced Latte" && ((SUCCESS++)) || ((FAILED++))
    upload_image "$CLIENT_ASSETS/Hot_Cold/Cold83.jpg" 8 "Cold Brew" && ((SUCCESS++)) || ((FAILED++))
    upload_image "$CLIENT_ASSETS/Hot_Cold/Cold1.jpg" 9 "Frappuccino" && ((SUCCESS++)) || ((FAILED++))
    echo ""
    
    # Pastries
    echo -e "${BLUE}Pastries:${NC}"
    upload_image "$CLIENT_ASSETS/Pastries_Specials/Almond Croissant.jpg" 10 "Croissant" && ((SUCCESS++)) || ((FAILED++))
    upload_image "$CLIENT_ASSETS/Pastries_Specials/Brown Butter Banana Bread.jpg" 11 "Chocolate Muffin" && ((SUCCESS++)) || ((FAILED++))
    upload_image "$CLIENT_ASSETS/Pastries_Specials/Matcha Scone.jpg" 12 "Blueberry Scone" && ((SUCCESS++)) || ((FAILED++))
    upload_image "$CLIENT_ASSETS/Pastries_Specials/special1.jpg" 13 "Cheesecake Slice" && ((SUCCESS++)) || ((FAILED++))
    echo ""
    
    # Specials
    echo -e "${BLUE}Specials:${NC}"
    upload_image "$CLIENT_ASSETS/Pastries_Specials/special2.jpg" 14 "Driftwood Special" && ((SUCCESS++)) || ((FAILED++))
    upload_image "$CLIENT_ASSETS/Pastries_Specials/special3.jpg" 15 "Seasonal Latte" && ((SUCCESS++)) || ((FAILED++))
    echo ""
    
    # Merchandise
    echo -e "${BLUE}Merchandise:${NC}"
    upload_image "$CLIENT_ASSETS/Merch/M3.jpeg" 16 "Driftwood Mug" && ((SUCCESS++)) || ((FAILED++))
    upload_image "$CLIENT_ASSETS/Merch/M1.jpeg" 17 "Coffee Beans" && ((SUCCESS++)) || ((FAILED++))
    echo ""
    
    echo -e "${BLUE}========================================${NC}"
    echo -e "${GREEN}✅ Successful uploads: $SUCCESS${NC}"
    echo -e "${RED}❌ Failed uploads: $FAILED${NC}"
    echo -e "${BLUE}========================================${NC}"

# Mode 2: Manual one by one
elif [ "$MODE" == "2" ]; then
    echo -e "${YELLOW}Manual upload mode${NC}"
    echo "Available products:"
    curl -s "$API_URL/api/products?per_page=100" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for p in data['data']:
    has_img = '✅' if p.get('image_url') else '❌'
    print(f\"{p['id']:2d}. {p['name']:25s} ({p['category_name']:15s}) {has_img}\")
"
    echo ""
    
    while true; do
        read -p "Enter product ID (or 'q' to quit): " PRODUCT_ID
        if [ "$PRODUCT_ID" == "q" ]; then
            break
        fi
        
        read -p "Enter image path: " IMAGE_PATH
        
        # Get product name
        PRODUCT_NAME=$(curl -s "$API_URL/api/products/$PRODUCT_ID" | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['name'])" 2>/dev/null)
        
        upload_image "$IMAGE_PATH" "$PRODUCT_ID" "$PRODUCT_NAME"
        echo ""
    done

# Mode 3: Single upload
elif [ "$MODE" == "3" ]; then
    echo -e "${YELLOW}Single image upload${NC}"
    echo ""
    
    read -p "Product ID: " PRODUCT_ID
    read -p "Image path: " IMAGE_PATH
    
    PRODUCT_NAME=$(curl -s "$API_URL/api/products/$PRODUCT_ID" | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['name'])" 2>/dev/null)
    
    upload_image "$IMAGE_PATH" "$PRODUCT_ID" "$PRODUCT_NAME"
fi

echo ""
echo -e "${GREEN}Done! Check your menu at http://localhost:5173${NC}"
