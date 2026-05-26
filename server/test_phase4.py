"""
Phase 4 API Test Script
Tests all newly implemented endpoints
"""
import requests
import json

BASE_URL = "http://localhost:5000/api"

def print_response(title, response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"TEST: {title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")
    print(f"{'='*60}\n")

def test_products():
    """Test product endpoints"""
    print("\n🛍️  TESTING PRODUCT ENDPOINTS")
    
    # 1. Get all products
    response = requests.get(f"{BASE_URL}/products")
    print_response("GET /api/products", response)
    
    # 2. Get featured products
    response = requests.get(f"{BASE_URL}/products/featured")
    print_response("GET /api/products/featured", response)
    
    # 3. Get product by ID
    response = requests.get(f"{BASE_URL}/products/1")
    print_response("GET /api/products/1", response)
    
    # 4. Get products by category
    response = requests.get(f"{BASE_URL}/products/category/1")
    print_response("GET /api/products/category/1", response)
    
    # 5. Search products
    response = requests.get(f"{BASE_URL}/products?search=coffee")
    print_response("GET /api/products?search=coffee", response)

def test_categories():
    """Test category endpoints"""
    print("\n📁 TESTING CATEGORY ENDPOINTS")
    
    # 1. Get all categories
    response = requests.get(f"{BASE_URL}/categories")
    print_response("GET /api/categories", response)
    
    # 2. Get category by ID
    response = requests.get(f"{BASE_URL}/categories/1")
    print_response("GET /api/categories/1", response)
    
    # 3. Get category products
    response = requests.get(f"{BASE_URL}/categories/1/products")
    print_response("GET /api/categories/1/products", response)

def test_guest_checkout():
    """Test guest checkout flow"""
    print("\n🛒 TESTING GUEST CHECKOUT FLOW")
    
    # 1. Create order (guest)
    order_data = {
        "items": [
            {"product_id": 1, "quantity": 2},
            {"product_id": 2, "quantity": 1}
        ],
        "order_type": "pickup",
        "payment_method": "cash"
    }
    response = requests.post(f"{BASE_URL}/orders", json=order_data)
    print_response("POST /api/orders (Guest Checkout)", response)
    
    if response.status_code == 201:
        order = response.json()['data']
        order_number = order['order_number']
        
        # 2. Track order by number
        response = requests.get(f"{BASE_URL}/orders/{order_number}")
        print_response(f"GET /api/orders/{order_number} (Track Order)", response)

def test_admin_login():
    """Test admin login and get token"""
    print("\n🔐 TESTING ADMIN LOGIN")
    
    login_data = {
        "email": "admin@driftwood.com",
        "password": "password123"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print_response("POST /api/auth/login (Admin)", response)
    
    if response.status_code == 200:
        token = response.json()['data']['access_token']
        return token
    return None

def test_admin_features(token):
    """Test admin endpoints"""
    if not token:
        print("⚠️  Skipping admin tests - no token")
        return
    
    print("\n👑 TESTING ADMIN FEATURES")
    headers = {"Authorization": f"Bearer {token}"}
    
    # 1. Create product
    product_data = {
        "name": "Test Coffee",
        "description": "A test coffee product",
        "price": 350,
        "category_id": 1,
        "stock_quantity": 100
    }
    response = requests.post(f"{BASE_URL}/products", json=product_data, headers=headers)
    print_response("POST /api/products (Create Product)", response)
    
    if response.status_code == 201:
        product_id = response.json()['data']['id']
        
        # 2. Update product
        update_data = {"price": 400}
        response = requests.put(f"{BASE_URL}/products/{product_id}", json=update_data, headers=headers)
        print_response(f"PUT /api/products/{product_id} (Update Product)", response)
        
        # 3. Update stock
        stock_data = {"quantity": 50}
        response = requests.put(f"{BASE_URL}/products/{product_id}/stock", json=stock_data, headers=headers)
        print_response(f"PUT /api/products/{product_id}/stock (Update Stock)", response)
        
        # 4. Delete product
        response = requests.delete(f"{BASE_URL}/products/{product_id}", headers=headers)
        print_response(f"DELETE /api/products/{product_id} (Delete Product)", response)
    
    # 5. Create category
    category_data = {
        "name": "Test Category",
        "description": "A test category"
    }
    response = requests.post(f"{BASE_URL}/categories", json=category_data, headers=headers)
    print_response("POST /api/categories (Create Category)", response)
    
    # 6. Get all orders (admin)
    response = requests.get(f"{BASE_URL}/orders", headers=headers)
    print_response("GET /api/orders (Admin View)", response)

def test_health():
    """Test health check"""
    print("\n❤️  TESTING HEALTH CHECK")
    response = requests.get(f"{BASE_URL}/health")
    print_response("GET /api/health", response)

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("PHASE 4 API TEST SUITE")
    print("="*60)
    
    try:
        # Test health first
        test_health()
        
        # Test public endpoints
        test_products()
        test_categories()
        test_guest_checkout()
        
        # Test admin features
        token = test_admin_login()
        test_admin_features(token)
        
        print("\n" + "="*60)
        print("✅ ALL TESTS COMPLETED")
        print("="*60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to server")
        print("Make sure the server is running: python run.py")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")

if __name__ == "__main__":
    main()
