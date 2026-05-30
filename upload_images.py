#!/usr/bin/env python3
"""
Driftwood Café - Image Upload Tool (Python)
Simple script to upload product images to the backend
"""

import requests
import os
import sys
from pathlib import Path

# Configuration
API_URL = "http://localhost:5000"
CLIENT_ASSETS = Path("client/src/assets")

# Color codes for terminal output
class Colors:
    BLUE = '\033[0;34m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    RED = '\033[0;31m'
    NC = '\033[0m'  # No Color

def print_header():
    print(f"{Colors.BLUE}{'='*50}{Colors.NC}")
    print(f"{Colors.BLUE}Driftwood Café - Image Upload Tool{Colors.NC}")
    print(f"{Colors.BLUE}{'='*50}{Colors.NC}\n")

def login(email="admin@driftwood.com", password="admin123"):
    """Login and get access token"""
    print(f"{Colors.YELLOW}Logging in...{Colors.NC}")
    
    try:
        response = requests.post(
            f"{API_URL}/api/auth/login",
            json={"email": email, "password": password}
        )
        
        if response.status_code == 200 and response.json().get('success'):
            token = response.json()['access_token']
            print(f"{Colors.GREEN}✅ Login successful!{Colors.NC}\n")
            return token
        else:
            print(f"{Colors.RED}❌ Login failed!{Colors.NC}")
            print(f"Response: {response.text}\n")
            print("Create an admin account first:")
            print(f"curl -X POST {API_URL}/api/auth/register \\")
            print("  -H 'Content-Type: application/json' \\")
            print("  -d '{\"email\":\"admin@driftwood.com\",\"password\":\"admin123\",\"full_name\":\"Admin\",\"phone\":\"+254700000000\",\"role\":\"admin\"}'")
            return None
    except Exception as e:
        print(f"{Colors.RED}❌ Error: {e}{Colors.NC}")
        return None

def upload_image(token, image_path, product_id, product_name):
    """Upload an image to a product"""
    if not os.path.exists(image_path):
        print(f"{Colors.RED}  ❌ File not found: {image_path}{Colors.NC}")
        return False
    
    print(f"{Colors.BLUE}  Uploading: {product_name} (ID: {product_id}){Colors.NC}")
    
    try:
        with open(image_path, 'rb') as f:
            files = {'file': f}
            data = {
                'product_id': product_id,
                'optimize': 'true',
                'create_thumbnails': 'true'
            }
            headers = {'Authorization': f'Bearer {token}'}
            
            response = requests.post(
                f"{API_URL}/api/upload/product-image",
                files=files,
                data=data,
                headers=headers
            )
            
            if response.status_code == 200 and response.json().get('success'):
                image_url = response.json()['data']['url']
                print(f"{Colors.GREEN}  ✅ Success! Image URL: {image_url}{Colors.NC}")
                return True
            else:
                error = response.json().get('error', 'Unknown error')
                print(f"{Colors.RED}  ❌ Failed: {error}{Colors.NC}")
                return False
    except Exception as e:
        print(f"{Colors.RED}  ❌ Error: {e}{Colors.NC}")
        return False

def upload_all_images(token):
    """Upload all images automatically"""
    print(f"{Colors.YELLOW}Uploading all images automatically...{Colors.NC}\n")
    
    # Image mappings: (image_path, product_id, product_name)
    mappings = [
        # Hot Coffee
        (CLIENT_ASSETS / "Hot_Cold/Hot1.jpg", 1, "Espresso"),
        (CLIENT_ASSETS / "Hot_Cold/Hot2.jpg", 2, "Americano"),
        (CLIENT_ASSETS / "Hot_Cold/Hot3.jpg", 3, "Cappuccino"),
        (CLIENT_ASSETS / "Hot_Cold/Hot1.jpg", 4, "Latte"),
        (CLIENT_ASSETS / "Hot_Cold/Hot2.jpg", 5, "Mocha"),
        
        # Cold Coffee
        (CLIENT_ASSETS / "Hot_Cold/Cold1.jpg", 6, "Iced Americano"),
        (CLIENT_ASSETS / "Hot_Cold/Cold2.jpg", 7, "Iced Latte"),
        (CLIENT_ASSETS / "Hot_Cold/Cold83.jpg", 8, "Cold Brew"),
        (CLIENT_ASSETS / "Hot_Cold/Cold1.jpg", 9, "Frappuccino"),
        
        # Pastries
        (CLIENT_ASSETS / "Pastries_Specials/Almond Croissant.jpg", 10, "Croissant"),
        (CLIENT_ASSETS / "Pastries_Specials/Brown Butter Banana Bread.jpg", 11, "Chocolate Muffin"),
        (CLIENT_ASSETS / "Pastries_Specials/Matcha Scone.jpg", 12, "Blueberry Scone"),
        (CLIENT_ASSETS / "Pastries_Specials/special1.jpg", 13, "Cheesecake Slice"),
        
        # Specials
        (CLIENT_ASSETS / "Pastries_Specials/special2.jpg", 14, "Driftwood Special"),
        (CLIENT_ASSETS / "Pastries_Specials/special3.jpg", 15, "Seasonal Latte"),
        
        # Merchandise
        (CLIENT_ASSETS / "Merch/M3.jpeg", 16, "Driftwood Mug"),
        (CLIENT_ASSETS / "Merch/M1.jpeg", 17, "Coffee Beans"),
    ]
    
    success = 0
    failed = 0
    
    categories = {
        "Hot Coffee": [1, 2, 3, 4, 5],
        "Cold Coffee": [6, 7, 8, 9],
        "Pastries": [10, 11, 12, 13],
        "Specials": [14, 15],
        "Merchandise": [16, 17]
    }
    
    for category, ids in categories.items():
        print(f"{Colors.BLUE}{category}:{Colors.NC}")
        for image_path, product_id, product_name in mappings:
            if product_id in ids:
                if upload_image(token, str(image_path), product_id, product_name):
                    success += 1
                else:
                    failed += 1
        print()
    
    print(f"{Colors.BLUE}{'='*50}{Colors.NC}")
    print(f"{Colors.GREEN}✅ Successful uploads: {success}{Colors.NC}")
    print(f"{Colors.RED}❌ Failed uploads: {failed}{Colors.NC}")
    print(f"{Colors.BLUE}{'='*50}{Colors.NC}")

def list_products(token):
    """List all products"""
    try:
        response = requests.get(f"{API_URL}/api/products?per_page=100")
        if response.status_code == 200:
            products = response.json()['data']
            print("\nAvailable products:")
            for p in products:
                has_img = "✅" if p.get('image_url') else "❌"
                print(f"{p['id']:2d}. {p['name']:25s} ({p['category_name']:15s}) {has_img}")
            print()
    except Exception as e:
        print(f"{Colors.RED}Error listing products: {e}{Colors.NC}")

def manual_upload(token):
    """Manual upload mode"""
    print(f"{Colors.YELLOW}Manual upload mode{Colors.NC}")
    list_products(token)
    
    while True:
        product_id = input("Enter product ID (or 'q' to quit): ")
        if product_id.lower() == 'q':
            break
        
        try:
            product_id = int(product_id)
        except ValueError:
            print(f"{Colors.RED}Invalid product ID{Colors.NC}")
            continue
        
        image_path = input("Enter image path: ")
        
        # Get product name
        try:
            response = requests.get(f"{API_URL}/api/products/{product_id}")
            if response.status_code == 200:
                product_name = response.json()['data']['name']
                upload_image(token, image_path, product_id, product_name)
            else:
                print(f"{Colors.RED}Product not found{Colors.NC}")
        except Exception as e:
            print(f"{Colors.RED}Error: {e}{Colors.NC}")
        
        print()

def main():
    print_header()
    
    # Login
    email = input("Email [admin@driftwood.com]: ").strip() or "admin@driftwood.com"
    password = input("Password [admin123]: ").strip() or "admin123"
    
    token = login(email, password)
    if not token:
        sys.exit(1)
    
    # Choose mode
    print(f"{Colors.YELLOW}Choose Upload Mode:{Colors.NC}")
    print("1) Upload all images automatically (recommended)")
    print("2) Upload images one by one (manual)")
    print("3) Exit")
    
    mode = input("Choose option [1]: ").strip() or "1"
    print()
    
    if mode == "1":
        upload_all_images(token)
    elif mode == "2":
        manual_upload(token)
    else:
        print("Exiting...")
        return
    
    print(f"\n{Colors.GREEN}Done! Check your menu at http://localhost:5173{Colors.NC}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Interrupted by user{Colors.NC}")
        sys.exit(0)
