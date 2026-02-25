# Automated Toll Collection System API Documentation

## Base URL
```
http://localhost:8000/api
```

---

## 1. Users Management

### Get All Users
**Endpoint:** `GET /users`

**Description:** Retrieve all registered user data.

**Response Example:**
```json
[
  {
    "user_id": "123",
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "1234567890"
  }
]
```

**Status Codes:**
- `200 OK` - Success

---

### Add New User
**Endpoint:** `POST /users`

**Description:** Add a new user to the system.

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "1234567890"
}
```

**Response Example:**
```json
{
  "message": "User added successfully",
  "user_id": "123"
}
```

**Status Codes:**
- `201 Created` - User created successfully
- `400 Bad Request` - Invalid input

---

### Delete User
**Endpoint:** `DELETE /users/{user_id}`

**Description:** Remove a user from the system.

**Response Example:**
```json
{
  "message": "User deleted successfully"
}
```

**Status Codes:**
- `200 OK` - User deleted successfully
- `404 Not Found` - User not found

---

## 2. User Vehicles

### Get Vehicle Data
**Endpoint:** `GET /user/car`

**Description:** Retrieve vehicle data for all users or a specific user.

**Query Parameters (Optional):**
- `user_id` – Filter vehicles by user.

**Example Request:**
```
GET /user/car?user_id=123
```

**Response Example:**
```json
[
  {
    "car_id": "1",
    "user_id": "123",
    "license_plate": "XYZ-987",
    "model": "Toyota Camry",
    "color": "Blue"
  }
]
```

**Status Codes:**
- `200 OK` - Success

---

### Add Vehicle
**Endpoint:** `POST /user/car`

**Description:** Add vehicle information for a user.

**Request Body:**
```json
{
  "user_id": 123,
  "license_plate": "XYZ-987",
  "model": "Toyota Camry",
  "color": "Blue",
  "vehicle_type": "car"
}
```

**Vehicle Types:** `car`, `truck`, `motorcycle`, `bus`, `minibus`, `van`

**Response Example:**
```json
{
  "message": "Vehicle added successfully",
  "car_id": "1"
}
```

**Status Codes:**
- `201 Created` - Vehicle created successfully
- `400 Bad Request` - Invalid input
- `404 Not Found` - User not found

---

### Delete Vehicle
**Endpoint:** `DELETE /user/car/{car_id}`

**Description:** Remove a vehicle from the system.

**Response Example:**
```json
{
  "message": "Vehicle deleted successfully"
}
```

**Status Codes:**
- `200 OK` - Vehicle deleted successfully
- `404 Not Found` - Vehicle not found

---

## 3. User Wallet

### Get Wallet Data
**Endpoint:** `GET /user/wallet`

**Description:** Retrieve wallet balance and transaction history for a user.

**Query Parameters:**
- `user_id` – The ID of the user. (Required)

**Example Request:**
```
GET /user/wallet?user_id=123
```

**Response Example:**
```json
{
  "user_id": "123",
  "balance": 250.75,
  "transactions": [
    {
      "transaction_id": "TXN001",
      "amount": 50.00,
      "transaction_type": "top-up",
      "date": "2026-02-25T10:00:00Z"
    }
  ]
}
```

**Status Codes:**
- `200 OK` - Success
- `400 Bad Request` - Missing user_id parameter
- `404 Not Found` - User or wallet not found

---

### Add Money to Wallet
**Endpoint:** `POST /user/wallet`

**Description:** Add money to the user's wallet.

**Request Body:**
```json
{
  "user_id": 123,
  "amount": 100.00
}
```

**Response Example:**
```json
{
  "message": "Wallet updated successfully",
  "new_balance": 350.75
}
```

**Status Codes:**
- `200 OK` - Funds added successfully
- `400 Bad Request` - Invalid input
- `404 Not Found` - User or wallet not found

---

## 4. Toll Capture (Gate)

### Capture Vehicle at Gate
**Endpoint:** `POST /capture/{gate_id}`

**Description:** Capture vehicle license plate at a toll gate, process billing, and notify the user.

**Path Parameters:**
- `gate_id` – The unique identifier of the gate.

**Request Body:**
```json
{
  "license_plate": "XYZ-987"
}
```

**Response Example:**
```json
{
  "message": "Toll captured successfully",
  "user_id": "123",
  "amount_charged": 5.50,
  "location": "Gate 01 - Highway 5",
  "timestamp": "2026-02-25T14:30:00Z"
}
```

**Status Codes:**
- `200 OK` - Toll captured successfully
- `400 Bad Request` - Invalid input
- `404 Not Found` - Gate or vehicle not found

---

## HTTP Status Codes Reference

| Code | Meaning |
|------|---------|
| `200 OK` | Successful request |
| `201 Created` | Resource created successfully |
| `400 Bad Request` | Invalid request data |
| `404 Not Found` | Resource not found |
| `500 Internal Server Error` | Server-side error |

---

## Date/Time Format

All date and time values follow the ISO 8601 format:
```
2026-02-25T14:30:00Z
```

---

## Example Usage

### Create a User
```bash
curl -X POST http://localhost:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "1234567890"
  }'
```

### Add a Vehicle
```bash
curl -X POST http://localhost:8000/api/user/car \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "license_plate": "ABC-123",
    "model": "Honda Civic",
    "color": "Red",
    "vehicle_type": "car"
  }'
```

### Get Wallet Balance
```bash
curl -X GET "http://localhost:8000/api/user/wallet?user_id=1"
```

### Add Funds to Wallet
```bash
curl -X POST http://localhost:8000/api/user/wallet \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "amount": 100.00
  }'
```

### Capture Toll
```bash
curl -X POST http://localhost:8000/api/capture/GATE01 \
  -H "Content-Type: application/json" \
  -d '{
    "license_plate": "ABC-123"
  }'
```

---

## Error Response Format

All error responses follow this format:
```json
{
  "error": "Description of the error",
  "details": "Additional information (if applicable)"
}
```

---

## Notes

- All endpoints accept and return JSON data.
- The API uses UTC timezone for all timestamps.
- Vehicle license plates are unique in the system.
- Users can have multiple vehicles.
- Toll charges are automatically deducted from the user's wallet balance.
