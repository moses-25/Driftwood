#!/usr/bin/env python3
"""
Test script to verify all backend routes are working
"""
import requests
import json

BASE_URL = "http://localhost:5000"

def test_health():
    """Test health check endpoint"""
    print("\n🔍 Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_contact_form():
    """Test contact form submission"""
    print("\n📧 Testing Contact Form...")
    try:
        data = {
            "name": "Test User",
            "email": "test@example.com",
            "phone": "+254712345678",
            "message": "This is a test message from the automated test script."
        }
        response = requests.post(f"{BASE_URL}/api/contact", json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_newsletter_subscription():
    """Test newsletter subscription"""
    print("\n📰 Testing Newsletter Subscription...")
    try:
        data = {"email": "newsletter@example.com"}
        response = requests.post(f"{BASE_URL}/api/notifications/newsletter/subscribe", json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_get_products():
    """Test get products endpoint"""
    print("\n🛍️  Testing Get Products...")
    try:
        response = requests.get(f"{BASE_URL}/api/products")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Products found: {len(data.get('data', []))}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_get_categories():
    """Test get categories endpoint"""
    print("\n📁 Testing Get Categories...")
    try:
        response = requests.get(f"{BASE_URL}/api/categories")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Categories found: {len(data.get('data', []))}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_create_order():
    """Test order creation (guest checkout)"""
    print("\n🛒 Testing Order Creation...")
    try:
        # First get a product
        products_response = requests.get(f"{BASE_URL}/api/products")
        if products_response.status_code != 200:
            print("❌ Cannot get products for order test")
            return False
        
        products = products_response.json().get('data', [])
        if not products:
            print("❌ No products available for order test")
            return False
        
        product = products[0]
        
        order_data = {
            "items": [
                {
                    "product_id": product['id'],
                    "quantity": 1,
                    "customizations": {}
                }
            ],
            "order_type": "pickup",
            "payment_method": "cash"
        }
        
        response = requests.post(f"{BASE_URL}/api/orders", json=order_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 201
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("BACKEND ROUTES TEST SUITE")
    print("="*60)
    
    tests = [
        ("Health Check", test_health),
        ("Contact Form", test_contact_form),
        ("Newsletter Subscription", test_newsletter_subscription),
        ("Get Products", test_get_products),
        ("Get Categories", test_get_categories),
        ("Create Order", test_create_order),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Test '{name}' crashed: {e}")
            results.append((name, False))
    
    print("\n" + "="*60)
    print("TEST RESULTS")
    print("="*60)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")

if __name__ == "__main__":
    main()
