# Automated Toll Collection System API Setup Guide

## Overview
This document provides instructions for setting up and running the Automated Toll Collection System API.

## Prerequisites
- Python 3.8+
- Django 5.2.7
- Django REST Framework
- SQLite3 (default database)

## Installation

### 1. Install Dependencies
All required packages are listed in `requirements.txt`. Install them with:

```bash
pip install -r requirements.txt
```

### 2. Database Setup

#### Apply Migrations
```bash
python manage.py migrate
```

#### Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account for accessing Django Admin at `/admin/`.

### 3. Load Sample Data

To populate the database with sample data for testing:

```bash
python manage.py shell < sample_data.py
```

This will create:
- 2 sample users (John Doe, Jane Smith)
- 2 sample vehicles
- 2 sample toll gates
- 2 toll types

## Running the Server

Start the development server:

```bash
python manage.py runserver
```

The API will be accessible at: `http://localhost:8000`

The admin interface will be at: `http://localhost:8000/admin`

## API Endpoints

### Base URL
```
http://localhost:8000/api
```

### 1. User Management
- `GET /users` - List all users
- `POST /users` - Create new user
- `DELETE /users/{user_id}` - Delete user

### 2. Vehicle Management
- `GET /user/car` - List all vehicles (optionally filter by user_id)
- `POST /user/car` - Add new vehicle
- `DELETE /user/car/{car_id}` - Delete vehicle

### 3. Wallet Management
- `GET /user/wallet?user_id={user_id}` - Get wallet balance and transactions
- `POST /user/wallet` - Add funds to wallet

### 4. Toll Capture
- `POST /capture/{gate_id}` - Capture vehicle at toll gate

## Testing the API

### Using cURL

#### 1. Get All Users
```bash
curl -X GET http://localhost:8000/api/users/
```

#### 2. Create a User
```bash
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "1234567890"
  }'
```

#### 3. Add a Vehicle
```bash
curl -X POST http://localhost:8000/api/user/car/ \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "license_plate": "ABC-123",
    "model": "Honda Civic",
    "color": "Red",
    "vehicle_type": "car"
  }'
```

#### 4. Get Wallet Balance
```bash
curl -X GET "http://localhost:8000/api/user/wallet?user_id=1"
```

#### 5. Add Funds to Wallet
```bash
curl -X POST http://localhost:8000/api/user/wallet \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "amount": 100.00
  }'
```

#### 6. Capture Toll
```bash
curl -X POST http://localhost:8000/api/capture/GATE01/ \
  -H "Content-Type: application/json" \
  -d '{
    "license_plate": "ABC-123"
  }'
```

### Using Postman

1. Import the API endpoints into Postman
2. Set the base URL to `http://localhost:8000/api`
3. Create requests for each endpoint
4. Test with sample data

## Project Structure

```
autofare/
├── autofare/              # Project settings
│   ├── settings.py        # Django configuration
│   ├── urls.py           # Main URL configuration
│   └── wsgi.py
├── users/                 # User management app
│   ├── models.py         # UserProfile, Wallet, Transaction models
│   ├── views.py          # API views
│   ├── serializers.py    # DRF serializers
│   └── urls.py           # App URL configuration
├── vehicles/             # Vehicle management app
│   ├── models.py         # Vehicle model
│   ├── views.py          # API views
│   ├── serializers.py    # DRF serializers
│   └── urls.py           # App URL configuration
├── toll/                 # Toll management app
│   ├── models.py         # Gate, Toll, Trip models
│   ├── views.py          # Toll capture views
│   ├── serializers.py    # DRF serializers
│   └── urls.py           # App URL configuration
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
├── API_DOCUMENTATION.md  # Complete API documentation
├── API_TEST_EXAMPLES.http # Test request examples
└── sample_data.py        # Sample data initialization
```

## Configuration

### Django Settings

Key settings in `autofare/settings.py`:

- **DEBUG**: Set to `False` in production
- **ALLOWED_HOSTS**: Add your domain/IP for production
- **DATABASES**: SQLite by default, change for production
- **REST_FRAMEWORK**: API settings including authentication and permissions
- **SIMPLE_JWT**: JWT token settings

### Environment Variables

For production, use environment variables:

```python
import os

SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = os.environ.get('DEBUG', False)
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')
```

## Common Issues and Solutions

### Issue: "No such table" error
**Solution**: Run migrations
```bash
python manage.py migrate
```

### Issue: Port 8000 already in use
**Solution**: Use a different port
```bash
python manage.py runserver 8001
```

### Issue: Module import errors
**Solution**: Ensure all dependencies are installed
```bash
pip install -r requirements.txt
```

### Issue: Static files not loading
**Solution**: Collect static files (for production)
```bash
python manage.py collectstatic
```

## Deployment

For production deployment:

1. Set `DEBUG = False` in settings
2. Update `ALLOWED_HOSTS` with your domain
3. Use a production database (PostgreSQL recommended)
4. Use a production web server (Gunicorn, uWSGI)
5. Use environment variables for sensitive data
6. Set up HTTPS/SSL
7. Configure proper logging
8. Set up backup strategy for database

### Example Gunicorn command:
```bash
gunicorn autofare.wsgi:application --bind 0.0.0.0:8000
```

## API Documentation

For complete API documentation, see [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

For example API requests, see [API_TEST_EXAMPLES.http](API_TEST_EXAMPLES.http)

## Support

For issues or questions:
1. Check the API documentation
2. Review the test examples
3. Check Django/DRF documentation
4. Run sample_data.py to ensure setup is correct

## Security Notes

- Change the default `SECRET_KEY` in production
- Use HTTPS/SSL for all API calls
- Implement rate limiting for production
- Add authentication/authorization as needed
- Validate all user inputs
- Use CORS headers if serving from different domains
- Keep dependencies updated

## Performance Tips

- Use pagination for large datasets
- Index frequently queried fields
- Cache frequently accessed data
- Use database query optimization
- Monitor API response times
- Implement logging for debugging
