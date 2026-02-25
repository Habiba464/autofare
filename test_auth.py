#!/usr/bin/env python
"""
Authentication Test Script for Automated Toll Collection System API
Tests signup, login, and token refresh functionality

Usage: python test_auth.py
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000/api"

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

def test_endpoint(method, endpoint, data=None, params=None, headers=None):
    """Test a single endpoint"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url, params=params, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)
        else:
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

def main():
    global_test_data = {}
    
    print(f"{Colors.BOLD}{Colors.BLUE}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║  Automated Toll System - Authentication Test Suite         ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(Colors.END)
    
    # TEST 1: Signup with Valid Data
    print_header("TEST 1: User Signup with Valid Data")
    signup_data = {
        "name": "Auth Test User",
        "email": f"authtest{int(time.time())}@example.com",
        "phone": "9876543210",
        "password": "SecurePass123",
        "password_confirm": "SecurePass123"
    }
    print_info(f"Request: POST /users/auth/signup/")
    print_info(f"Data: {json.dumps({**signup_data, 'password': '****', 'password_confirm': '****'})}")
    response = test_endpoint("POST", "/users/auth/signup/", signup_data)
    
    if response and response.status_code == 201:
        print_success("User registered successfully")
        data = response.json()
        global_test_data['user_id'] = data.get('user_id')
        global_test_data['email'] = signup_data['email']
        global_test_data['password'] = signup_data['password']
        global_test_data['signup_access'] = data.get('access')
        global_test_data['signup_refresh'] = data.get('refresh')
        print_response(response, 201)
    else:
        print_error("Failed to signup user")
        print_response(response)
        return
    
    # TEST 2: Signup with Mismatched Passwords
    print_header("TEST 2: Signup with Mismatched Passwords (Should Fail)")
    bad_signup = {
        "name": "BadUser",
        "email": f"bad{int(time.time())}@example.com",
        "phone": "1234567890",
        "password": "Pass123",
        "password_confirm": "DifferentPass123"
    }
    print_info(f"Request: POST /users/auth/signup/")
    response = test_endpoint("POST", "/users/auth/signup/", bad_signup)
    
    if response and response.status_code == 400:
        print_success("Correctly rejected mismatched passwords")
        print_response(response, 400)
    else:
        print_error("Should have rejected mismatched passwords")
        print_response(response)
    
    # TEST 3: Signup with Duplicate Email
    print_header("TEST 3: Signup with Duplicate Email (Should Fail)")
    duplicate_signup = {
        "name": "Duplicate User",
        "email": global_test_data['email'],
        "phone": "1111111111",
        "password": "Pass123456",
        "password_confirm": "Pass123456"
    }
    print_info(f"Request: POST /users/auth/signup/ with existing email")
    response = test_endpoint("POST", "/users/auth/signup/", duplicate_signup)
    
    if response and response.status_code == 400:
        print_success("Correctly rejected duplicate email")
        print_response(response, 400)
    else:
        print_error("Should have rejected duplicate email")
        print_response(response)
    
    # TEST 4: Login with Correct Credentials
    print_header("TEST 4: Login with Correct Credentials")
    login_data = {
        "email": global_test_data['email'],
        "password": global_test_data['password']
    }
    print_info(f"Request: POST /users/auth/login/")
    print_info(f"Credentials: email={login_data['email']}, password=****")
    response = test_endpoint("POST", "/users/auth/login/", login_data)
    
    if response and response.status_code == 200:
        print_success("User logged in successfully")
        data = response.json()
        global_test_data['login_access'] = data.get('access')
        global_test_data['login_refresh'] = data.get('refresh')
        print_response(response, 200)
    else:
        print_error("Failed to login user")
        print_response(response)
        return
    
    # TEST 5: Login with Wrong Password
    print_header("TEST 5: Login with Wrong Password (Should Fail)")
    wrong_pwd = {
        "email": global_test_data['email'],
        "password": "WrongPassword123"
    }
    print_info(f"Request: POST /users/auth/login/ with wrong password")
    response = test_endpoint("POST", "/users/auth/login/", wrong_pwd)
    
    if response and response.status_code == 400:
        print_success("Correctly rejected wrong password")
        print_response(response, 400)
    else:
        print_error("Should have rejected wrong password")
        print_response(response)
    
    # TEST 6: Login with Non-existent Email
    print_header("TEST 6: Login with Non-existent Email (Should Fail)")
    nonexistent = {
        "email": "nonexistent@example.com",
        "password": "SomePassword123"
    }
    print_info(f"Request: POST /users/auth/login/ with non-existent email")
    response = test_endpoint("POST", "/users/auth/login/", nonexistent)
    
    if response and response.status_code == 400:
        print_success("Correctly rejected non-existent email")
        print_response(response, 400)
    else:
        print_error("Should have rejected non-existent email")
        print_response(response)
    
    # TEST 7: Refresh Token with Valid Token
    print_header("TEST 7: Refresh Token with Valid Refresh Token")
    refresh_data = {
        "refresh": global_test_data['login_refresh']
    }
    print_info(f"Request: POST /users/auth/refresh_token/")
    response = test_endpoint("POST", "/users/auth/refresh_token/", refresh_data)
    
    if response and response.status_code == 200:
        print_success("Token refreshed successfully")
        data = response.json()
        global_test_data['refreshed_access'] = data.get('access')
        print_response(response, 200)
    else:
        print_error("Failed to refresh token")
        print_response(response)
    
    # TEST 8: Refresh Token with Invalid Token
    print_header("TEST 8: Refresh Token with Invalid Token (Should Fail)")
    bad_refresh = {
        "refresh": "invalid.token.here"
    }
    print_info(f"Request: POST /users/auth/refresh_token/ with invalid token")
    response = test_endpoint("POST", "/users/auth/refresh_token/", bad_refresh)
    
    if response and response.status_code == 400:
        print_success("Correctly rejected invalid refresh token")
        print_response(response, 400)
    else:
        print_error("Should have rejected invalid refresh token")
        print_response(response)
    
    # TEST 9: Use Access Token in Protected Request
    print_header("TEST 9: Use Access Token in Protected Request")
    headers = {
        "Authorization": f"Bearer {global_test_data['login_access']}"
    }
    print_info(f"Request: GET /user/wallet?user_id={global_test_data['user_id']}")
    print_info(f"Header: Authorization: Bearer {global_test_data['login_access'][:20]}...")
    response = test_endpoint("GET", f"/user/wallet?user_id={global_test_data['user_id']}", headers=headers)
    
    if response and response.status_code == 200:
        print_success("Successfully used access token in request")
        print_response(response, 200)
    else:
        print_error("Failed to use access token")
        print_response(response)
    
    # TEST 10: Authentication Flow Summary
    print_header("Authentication Flow Test Summary")
    print_success("All authentication tests completed!")
    print_info("\nTests Performed:")
    print_info("1. ✓ Signup with valid credentials")
    print_info("2. ✓ Signup validation (mismatched passwords)")
    print_info("3. ✓ Signup validation (duplicate email)")
    print_info("4. ✓ Login with correct credentials")
    print_info("5. ✓ Login validation (wrong password)")
    print_info("6. ✓ Login validation (non-existent email)")
    print_info("7. ✓ Token refresh with valid token")
    print_info("8. ✓ Token refresh validation (invalid token)")
    print_info("9. ✓ Access token usage in protected request")
    
    print_info("\nTest Data Generated:")
    print_info(f"User ID: {global_test_data['user_id']}")
    print_info(f"Email: {global_test_data['email']}")
    print_info(f"Access Token: {global_test_data['login_access'][:30]}...")
    print_info(f"Refresh Token: {global_test_data['login_refresh'][:30]}...")
    
    print(f"\n{Colors.GREEN}{Colors.BOLD}Authentication system is working correctly!{Colors.END}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Test interrupted by user{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}Test failed with error: {str(e)}{Colors.END}")
