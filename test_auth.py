#!/usr/bin/env python3
"""Test authentication flow"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_authentication():
    print("Testing authentication flow...")
    print("-" * 40)
    
    # Test 1: Try to access protected route without auth
    print("1. Testing access without authentication...")
    response = requests.get(f"{BASE_URL}/")
    print(f"   Status: {response.status_code}")
    if response.status_code == 307:  # Redirect to login
        print("   ✓ Correctly redirected to login page")
    else:
        print("   ✗ Expected redirect to login")
    
    # Test 2: Try to access API without auth
    print("\n2. Testing API access without authentication...")
    response = requests.get(f"{BASE_URL}/api/events")
    print(f"   Status: {response.status_code}")
    if response.status_code == 401:
        print("   ✓ Correctly denied access")
    else:
        print("   ✗ Expected 401 Unauthorized")
    
    # Test 3: Login with test credentials
    print("\n3. Testing login...")
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    response = requests.post(
        f"{BASE_URL}/api/login",
        data=login_data
    )
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        token_data = response.json()
        token = token_data.get("access_token")
        print("   ✓ Login successful")
        print(f"   Token: {token[:20]}...")
        
        # Test 4: Access protected API with token
        print("\n4. Testing API access with authentication...")
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/api/events", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✓ Successfully accessed protected API")
            events = response.json()
            print(f"   Events count: {len(events)} date keys")
        else:
            print("   ✗ Failed to access API with token")
    else:
        print("   ✗ Login failed")
        print(f"   Error: {response.text}")

if __name__ == "__main__":
    try:
        test_authentication()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to server. Make sure the app is running on http://localhost:8000")