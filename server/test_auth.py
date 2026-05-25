"""
Test script for authentication endpoints
"""
import requests
import json

BASE_URL = "http://localhost:5000/api"

def print_response(title, response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")

def test_auth_flow():
    """Test complete authentication flow"""
    
    # Test 1: Register a new user
    print("\n🔹 TEST 1: Register New User")
    register_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "Test@1234",
        "first_name": "Test",
        "last_name": "User",
        "phone": "+254712345678"
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    print_response("Register Response", response)
    
    if response.status_code == 201:
        data = response.json()
        access_token = data['data']['access_token']
        refresh_token = data['data']['refresh_token']
        print(f"\n✅ Registration successful!")
        print(f"Access Token: {access_token[:50]}...")
        print(f"Refresh Token: {refresh_token[:50]}...")
    else:
        print("\n❌ Registration failed!")
        return
    
    # Test 2: Login with the registered user
    print("\n🔹 TEST 2: Login User")
    login_data = {
        "email": "testuser@example.com",
        "password": "Test@1234"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print_response("Login Response", response)
    
    if response.status_code == 200:
        data = response.json()
        access_token = data['data']['access_token']
        refresh_token = data['data']['refresh_token']
        print(f"\n✅ Login successful!")
    else:
        print("\n❌ Login failed!")
        return
    
    # Test 3: Get current user info
    print("\n🔹 TEST 3: Get Current User Info")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    print_response("Current User Response", response)
    
    # Test 4: Refresh access token
    print("\n🔹 TEST 4: Refresh Access Token")
    headers = {"Authorization": f"Bearer {refresh_token}"}
    response = requests.post(f"{BASE_URL}/auth/refresh", headers=headers)
    print_response("Refresh Token Response", response)
    
    if response.status_code == 200:
        data = response.json()
        new_access_token = data['data']['access_token']
        print(f"\n✅ Token refresh successful!")
        print(f"New Access Token: {new_access_token[:50]}...")
        access_token = new_access_token
    
    # Test 5: Change password
    print("\n🔹 TEST 5: Change Password")
    headers = {"Authorization": f"Bearer {access_token}"}
    change_password_data = {
        "old_password": "Test@1234",
        "new_password": "NewTest@5678"
    }
    response = requests.post(f"{BASE_URL}/auth/change-password", json=change_password_data, headers=headers)
    print_response("Change Password Response", response)
    
    # Test 6: Login with new password
    print("\n🔹 TEST 6: Login with New Password")
    login_data = {
        "email": "testuser@example.com",
        "password": "NewTest@5678"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print_response("Login with New Password Response", response)
    
    # Test 7: Request password reset
    print("\n🔹 TEST 7: Request Password Reset")
    reset_request_data = {
        "email": "testuser@example.com"
    }
    response = requests.post(f"{BASE_URL}/auth/request-password-reset", json=reset_request_data)
    print_response("Password Reset Request Response", response)
    
    if response.status_code == 200:
        data = response.json()
        if 'reset_token' in data:
            reset_token = data['reset_token']
            print(f"\n✅ Reset token generated!")
            
            # Test 8: Reset password with token
            print("\n🔹 TEST 8: Reset Password with Token")
            headers = {"Authorization": f"Bearer {reset_token}"}
            reset_password_data = {
                "new_password": "Reset@9999"
            }
            response = requests.post(f"{BASE_URL}/auth/reset-password", json=reset_password_data, headers=headers)
            print_response("Reset Password Response", response)
    
    # Test 9: Test invalid credentials
    print("\n🔹 TEST 9: Test Invalid Credentials")
    login_data = {
        "email": "testuser@example.com",
        "password": "WrongPassword123"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print_response("Invalid Login Response", response)
    
    # Test 10: Test duplicate registration
    print("\n🔹 TEST 10: Test Duplicate Registration")
    response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    print_response("Duplicate Registration Response", response)
    
    print("\n" + "="*60)
    print("✅ All authentication tests completed!")
    print("="*60)

if __name__ == "__main__":
    print("🚀 Starting Authentication Tests...")
    print(f"Base URL: {BASE_URL}")
    
    try:
        test_auth_flow()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to the server.")
        print("Make sure the Flask server is running on http://localhost:5000")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
