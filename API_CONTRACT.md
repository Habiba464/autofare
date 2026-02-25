# Automated Toll Collection System - API Contract

**Base URL:** `http://localhost:8000/api`  
**Version:** 1.0  
**Date:** February 25, 2026

---

## Table of Contents
1. [Authentication](#authentication)
2. [User Management](#user-management)
3. [Vehicle Management](#vehicle-management)
4. [Wallet Management](#wallet-management)
5. [Toll Operations](#toll-operations)

---

## Authentication

### 1. User Signup
Register a new user with credentials.

**Endpoint:** `POST /users/auth/signup/`

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "string (max 100 chars)",
  "email": "string (valid email)",
  "phone": "string (max 20 chars)",
  "password": "string (min 8 chars)",
  "password_confirm": "string (must match password)"
}
```

**Response (201 Created):**
```json
{
  "message": "User registered successfully",
  "user_id": "string",
  "email": "string",
  "access": "string (JWT access token, 60 min lifetime)",
  "refresh": "string (JWT refresh token, 7 day lifetime)"
}
```

**Response (400 Bad Request):**
```json
{
  "password": ["Passwords must match."],
  "email": ["Email already registered."]
}
```

**Example CURL:**
```bash
curl -X POST http://localhost:8000/api/users/auth/signup/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "9876543210",
    "password": "SecurePass123",
    "password_confirm": "SecurePass123"
  }'
```

**Example PowerShell:**
```powershell
$body = @{
    name = 'John Doe'
    email = 'john@example.com'
    phone = '9876543210'
    password = 'SecurePass123'
    password_confirm = 'SecurePass123'
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/users/auth/signup/" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $body
```

---

### 2. User Login
Authenticate user and get JWT tokens.

**Endpoint:** `POST /users/auth/login/`

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "email": "string",
  "password": "string"
}
```

**Response (200 OK):**
```json
{
  "message": "Login successful",
  "user_id": "string",
  "name": "string",
  "email": "string",
  "phone": "string",
  "access": "string (JWT access token)",
  "refresh": "string (JWT refresh token)"
}
```

**Response (400 Bad Request):**
```json
{
  "non_field_errors": ["Invalid email or password."]
}
```

**Example PowerShell:**
```powershell
$body = @{
    email = 'john@example.com'
    password = 'SecurePass123'
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/users/auth/login/" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $body
```

---

### 3. Refresh Access Token
Get a new access token using refresh token.

**Endpoint:** `POST /users/auth/refresh_token/`

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "refresh": "string (refresh token from login/signup)"
}
```

**Response (200 OK):**
```json
{
  "access": "string (new JWT access token)"
}
```

**Response (400 Bad Request):**
```json
{
  "detail": "Token is invalid or expired"
}
```

---

## User Management

### 1. List All Users
Get list of all registered users.

**Endpoint:** `GET /users/`

**Request Headers:**
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "username": "string",
    "email": "string",
    "profile": {
      "user_id": "1",
      "name": "string",
      "email": "string",
      "phone": "string"
    }
  }
]
```

**Example PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/users/" `
    -Method GET `
    -Headers @{"Authorization"="Bearer YOUR_ACCESS_TOKEN"}
```

---

### 2. Create User (Legacy - No Password)
Create a user without password registration.

**Endpoint:** `POST /users/`

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "string",
  "email": "string",
  "phone": "string"
}
```

**Response (201 Created):**
```json
{
  "id": "integer",
  "username": "string (auto-generated from email)",
  "email": "string"
}
```

---

### 3. Delete User
Delete a user by ID.

**Endpoint:** `DELETE /users/{user_id}/`

**Request Headers:**
```
Authorization: Bearer {access_token}
```

**Response (204 No Content):**
```
(empty body)
```

---

## Vehicle Management

### 1. List All Vehicles
Get list of all registered vehicles.

**Endpoint:** `GET /user/car/`

**Request Headers:**
```
Authorization: Bearer {access_token}
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "vehicle_license_plate": "ABC123",
    "vehicle_color": "Red",
    "vehicle_model": "Toyota Camry",
    "vehicle_type": "Sedan"
  }
]
```

---

### 2. Create Vehicle
Register a new vehicle.

**Endpoint:** `POST /user/car/`

**Request Headers:**
```
Content-Type: application/json
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "user_id": "integer",
  "vehicle_license_plate": "string",
  "vehicle_color": "string",
  "vehicle_model": "string",
  "vehicle_type": "string"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "user_id": 1,
  "vehicle_license_plate": "ABC123",
  "vehicle_color": "Red",
  "vehicle_model": "Toyota Camry",
  "vehicle_type": "Sedan"
}
```

---

### 3. Delete Vehicle
Delete a vehicle by ID.

**Endpoint:** `DELETE /user/car/{vehicle_id}/`

**Request Headers:**
```
Authorization: Bearer {access_token}
```

**Response (204 No Content):**
```
(empty body)
```

---

## Wallet Management

### 1. Get Wallet Balance & Transactions
Get user's wallet balance and transaction history.

**Endpoint:** `GET /wallet/{user_id}/`

**Request Headers:**
```
Authorization: Bearer {access_token}
```

**Response (200 OK):**
```json
{
  "user_id": "string",
  "balance": "decimal (2 places)",
  "transactions": [
    {
      "transaction_id": "string",
      "amount": "decimal (2 places)",
      "transaction_type": "string (CREDIT/DEBIT)",
      "date": "ISO 8601 datetime"
    }
  ]
}
```

---

### 2. Add Funds to Wallet
Add money to user's wallet.

**Endpoint:** `POST /wallet/add_funds/`

**Request Headers:**
```
Content-Type: application/json
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "user_id": "integer",
  "amount": "decimal (positive value)"
}
```

**Response (201 Created):**
```json
{
  "message": "Funds added successfully",
  "wallet_id": "integer",
  "new_balance": "decimal",
  "amount_added": "decimal"
}
```

---

## Toll Operations

### 1. Capture Toll
Record a vehicle passing through a toll gate.

**Endpoint:** `POST /capture/{gate_id}/`

**Request Headers:**
```
Content-Type: application/json
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "license_plate": "string",
  "vehicle_type": "string",
  "timestamp": "ISO 8601 datetime"
}
```

**Response (201 Created):**
```json
{
  "message": "Toll captured successfully",
  "toll_id": "string",
  "trip_id": "string",
  "amount_charged": "decimal",
  "vehicle_license_plate": "string",
  "gate_id": "integer",
  "timestamp": "ISO 8601 datetime"
}
```

**Response (400 Bad Request):**
```json
{
  "error": "Vehicle not found or insufficient wallet balance"
}
```

---

## Authentication

All protected endpoints require the `Authorization` header with a valid JWT access token:

```
Authorization: Bearer {access_token}
```

**Token Lifetime:**
- **Access Token:** 60 minutes
- **Refresh Token:** 7 days

**Token Type:** JWT (JSON Web Token)  
**Algorithm:** HS256  
**Signing Key:** Django SECRET_KEY

---

## Error Responses

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 204 | No Content - Success with no response body |
| 400 | Bad Request - Invalid request data |
| 401 | Unauthorized - Missing or invalid authentication |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource not found |
| 500 | Internal Server Error |

---

## Data Types

| Type | Format | Example |
|------|--------|---------|
| string | Text | "John Doe" |
| integer | Whole number | 42 |
| decimal | 2 decimal places | 99.99 |
| ISO 8601 datetime | YYYY-MM-DDTHH:MM:SSZ | 2026-02-25T14:30:45Z |
| JWT token | Bearer token | eyJhbGciOiJIUzI1NiIs... |

---

## Rate Limiting

No rate limiting currently implemented.

---

## CORS

CORS is enabled for cross-origin requests.

---

## Database Models

### User (Django built-in)
- `id` (PK)
- `username` (unique)
- `email` (unique)
- `password` (hashed with PBKDF2)
- `is_active` (boolean)

### UserProfile
- `user` (OneToOne FK to User)
- `name` (max 100 chars)
- `email` (unique)
- `phone` (max 20 chars)
- `national_id` (unique, nullable)

### Wallet
- `user` (OneToOne FK to User)
- `wallet_balance` (decimal)

### Transaction
- `wallet` (FK to Wallet)
- `transaction_id` (unique)
- `amount` (decimal)
- `transaction_type` (CREDIT/DEBIT)
- `date` (auto timestamp)

### Vehicle
- `user` (FK to User)
- `vehicle_license_plate` (unique)
- `vehicle_color`
- `vehicle_model`
- `vehicle_type`

### Gate
- `gate_id` (PK)
- `location` (text)

### Toll
- `vehicle` (FK to Vehicle)
- `gate` (FK to Gate)
- `toll_amount` (decimal)
- `timestamp` (datetime)

### Trip
- `vehicle` (FK to Vehicle)
- `start_gate` (FK to Gate)
- `end_gate` (FK to Gate)
- `distance` (decimal)
- `amount_charged` (decimal)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-25 | Initial API release with JWT authentication |

