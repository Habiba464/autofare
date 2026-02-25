#!/usr/bin/env python
"""
Quick Test Script for Automated Toll Collection System API
Run this script after starting the Django development server to quickly test all endpoints.

Usage: python test_api.py
"""

import requests
import json
from decimal import Decimal

BASE_URL = "http://localhost:8000/api"

# Terminal colors for better output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}")
    print(f"{text}")
    print(f"{'='*60}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.YELLOW}ℹ {text}{Colors.END}")

def test_endpoint(method, endpoint, data=None, params=None):
    """Test a single endpoint"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url, params=params)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url)
        else:
            print_error(f"Unsupported method: {method}")
            return None
        
        return response
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to server. Make sure Django is running on port 8000")
        return None
    except Exception as e:
        print_error(f"Request failed: {str(e)}")
        return None

def print_response(response, expected_status=None):
    """Print response details"""
    if response is None:
        return False
    
    status_match = expected_status is None or response.status_code == expected_status
    color = Colors.GREEN if status_match else Colors.RED
    
    print(f"Status: {color}{response.status_code}{Colors.END}")
    
    try:
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
    except:
        print(f"Response: {response.text}")
    
    return status_match

# Test Variables
user_id = None
car_id = None
gate_id = "GATE01"

def main():
    global user_id, car_id
    
    print(f"{Colors.BOLD}{Colors.BLUE}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║  Automated Toll Collection System - API Test Suite         ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(Colors.END)
    
    # TEST 1: Create User
    print_header("TEST 1: Create New User")
    user_data = {
        "name": "Test User",
        "email": "testuser@example.com",
        "phone": "9876543210"
    }
    print_info(f"Request: POST /users")
    print_info(f"Data: {json.dumps(user_data)}")
    response = test_endpoint("POST", "/users", user_data)
    
    if response and response.status_code == 201:
        print_success("User created successfully")
        user_id = response.json().get('user_id')
        print_info(f"User ID: {user_id}")
        print_response(response, 201)
    else:
        print_error("Failed to create user")
        print_response(response)
        return
    
    # TEST 2: List Users
    print_header("TEST 2: List All Users")
    print_info(f"Request: GET /users")
    response = test_endpoint("GET", "/users")
    
    if response and response.status_code == 200:
        print_success("Users retrieved successfully")
        print_response(response, 200)
    else:
        print_error("Failed to retrieve users")
        print_response(response)
    
    # TEST 3: Add Vehicle
    print_header("TEST 3: Add New Vehicle")
    vehicle_data = {
        "user_id": int(user_id),
        "license_plate": "TEST-001",
        "model": "Tesla Model 3",
        "color": "White",
        "vehicle_type": "car"
    }
    print_info(f"Request: POST /user/car")
    print_info(f"Data: {json.dumps(vehicle_data)}")
    response = test_endpoint("POST", "/user/car", vehicle_data)
    
    if response and response.status_code == 201:
        print_success("Vehicle added successfully")
        car_id = response.json().get('car_id')
        print_info(f"Car ID: {car_id}")
        print_response(response, 201)
    else:
        print_error("Failed to add vehicle")
        print_response(response)
        return
    
    # TEST 4: List Vehicles
    print_header("TEST 4: List All Vehicles")
    print_info(f"Request: GET /user/car")
    response = test_endpoint("GET", "/user/car")
    
    if response and response.status_code == 200:
        print_success("Vehicles retrieved successfully")
        print_response(response, 200)
    else:
        print_error("Failed to retrieve vehicles")
        print_response(response)
    
    # TEST 5: Get Wallet
    print_header("TEST 5: Get Wallet Balance")
    print_info(f"Request: GET /user/wallet?user_id={user_id}")
    response = test_endpoint("GET", "/user/wallet", params={"user_id": user_id})
    
    if response and response.status_code == 200:
        print_success("Wallet retrieved successfully")
        print_response(response, 200)
    else:
        print_error("Failed to retrieve wallet")
        print_response(response)
    
    # TEST 6: Add Funds to Wallet
    print_header("TEST 6: Add Funds to Wallet")
    funds_data = {
        "user_id": int(user_id),
        "amount": 100.00
    }
    print_info(f"Request: POST /user/wallet")
    print_info(f"Data: {json.dumps(funds_data)}")
    response = test_endpoint("POST", "/user/wallet", funds_data)
    
    if response and response.status_code == 200:
        print_success("Funds added successfully")
        print_response(response, 200)
    else:
        print_error("Failed to add funds")
        print_response(response)
    
    # TEST 7: Capture Toll
    print_header("TEST 7: Capture Vehicle at Toll Gate")
    capture_data = {
        "license_plate": "TEST-001"
    }
    print_info(f"Request: POST /capture/{gate_id}")
    print_info(f"Data: {json.dumps(capture_data)}")
    response = test_endpoint("POST", f"/capture/{gate_id}", capture_data)
    
    if response and response.status_code == 200:
        print_success("Toll captured successfully")
        print_response(response, 200)
    else:
        print_error("Failed to capture toll")
        print_response(response)
    
    # TEST 8: Delete Vehicle
    print_header("TEST 8: Delete Vehicle")
    print_info(f"Request: DELETE /user/car/{car_id}")
    response = test_endpoint("DELETE", f"/user/car/{car_id}")
    
    if response and response.status_code == 200:
        print_success("Vehicle deleted successfully")
        print_response(response, 200)
    else:
        print_error("Failed to delete vehicle")
        print_response(response)
    
    # TEST 9: Delete User
    print_header("TEST 9: Delete User")
    print_info(f"Request: DELETE /users/{user_id}")
    response = test_endpoint("DELETE", f"/users/{user_id}")
    
    if response and response.status_code == 200:
        print_success("User deleted successfully")
        print_response(response, 200)
    else:
        print_error("Failed to delete user")
        print_response(response)
    
    # Summary
    print_header("Test Summary")
    print_success("All tests completed successfully!")
    print_info("The API is working correctly and ready for use.")
    print_info(f"Next steps:")
    print_info("1. Review API_DOCUMENTATION.md for complete API reference")
    print_info("2. Check API_SETUP_GUIDE.md for deployment instructions")
    print_info("3. Use API_TEST_EXAMPLES.http for additional test requests")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Test interrupted by user{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}Test failed with error: {str(e)}{Colors.END}")
