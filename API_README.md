# Automated Toll Collection System API

A complete REST API implementation for managing toll collection, user accounts, vehicles, and wallet transactions.

## 🎯 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Apply database migrations
python manage.py migrate

# 3. Load sample data
python manage.py shell < sample_data.py

# 4. Start development server
python manage.py runserver

# 5. Test the API (in another terminal)
python test_api.py
```

The API will be available at: **http://localhost:8000/api**

## 📋 API Overview

### Base URL
```
http://localhost:8000/api
```

### Available Endpoints

#### 👥 User Management
- `GET /users` - List all users
- `POST /users` - Create new user
- `DELETE /users/{user_id}` - Delete user

#### 🚗 Vehicle Management
- `GET /user/car` - List all vehicles (optionally filter by user_id)
- `POST /user/car` - Add new vehicle
- `DELETE /user/car/{car_id}` - Delete vehicle

#### 💳 Wallet Management
- `GET /user/wallet?user_id=1` - Get wallet balance and transactions
- `POST /user/wallet` - Add funds to wallet

#### 🛣️ Toll Capture
- `POST /capture/{gate_id}` - Capture vehicle at toll gate

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [API_DOCUMENTATION.md](API_DOCUMENTATION.md) | Complete API reference with all endpoints |
| [API_SETUP_GUIDE.md](API_SETUP_GUIDE.md) | Installation, setup, and deployment guide |
| [API_TEST_EXAMPLES.http](API_TEST_EXAMPLES.http) | HTTP request examples for testing |
| [API_IMPLEMENTATION_SUMMARY.md](API_IMPLEMENTATION_SUMMARY.md) | Implementation details and features |
| [IMPLEMENTATION_CHECKLIST.md](IMPLEMENTATION_CHECKLIST.md) | Verification checklist |

## 🧪 Testing

### Quick Test with Python Script
```bash
python test_api.py
```

### Verify Setup
```bash
python verify_setup.py
```

### Using cURL
```bash
# Get all users
curl -X GET http://localhost:8000/api/users/

# Create a user
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "1234567890"
  }'
```

## 🛠️ Technologies Used

- **Django** 5.2.7 - Web framework
- **Django REST Framework** - REST API toolkit
- **Django REST Framework SimpleJWT** - JWT authentication
- **SQLite3** - Default database
- **Python** 3.8+

## 📁 Project Structure

```
autofare/
├── users/
│   ├── models.py           # User, Wallet, Transaction models
│   ├── views.py            # API endpoints
│   ├── serializers.py      # Data serialization
│   └── urls.py             # URL routing
├── vehicles/
│   ├── models.py           # Vehicle model
│   ├── views.py            # API endpoints
│   ├── serializers.py      # Data serialization
│   └── urls.py             # URL routing
├── toll/
│   ├── models.py           # Gate, Toll, Trip models
│   ├── views.py            # Toll capture endpoints
│   ├── serializers.py      # Data serialization
│   └── urls.py             # URL routing
├── autofare/
│   ├── settings.py         # Django configuration
│   ├── urls.py             # Main URL router
│   ├── wsgi.py             # WSGI application
│   └── asgi.py             # ASGI application
├── manage.py               # Django management
├── requirements.txt        # Dependencies
└── [Documentation files]
```

## 🚀 Features

### User Management
- ✅ Create users with email validation
- ✅ Automatic wallet creation
- ✅ User profile management
- ✅ User deletion with cascading cleanup

### Vehicle Management
- ✅ Register vehicles per user
- ✅ Support multiple vehicle types
- ✅ License plate uniqueness
- ✅ Vehicle search and filtering

### Wallet System
- ✅ Wallet balance tracking
- ✅ Transaction history
- ✅ Add funds (top-up)
- ✅ Automatic toll deductions
- ✅ Transaction logging

### Toll Capture
- ✅ Gate-based toll processing
- ✅ Automatic fare calculation
- ✅ Balance validation
- ✅ Payment status tracking
- ✅ Transaction recording

## 📊 Response Format

All responses follow this format:

### Success Response
```json
{
  "message": "Operation successful",
  "data": {
    "user_id": "1",
    "name": "John Doe"
  }
}
```

### Error Response
```json
{
  "error": "Error message",
  "details": "Additional information"
}
```

## 🔒 Security

- ✅ Input validation
- ✅ Email format validation
- ✅ CSRF protection
- ✅ Atomic database transactions
- ✅ SQL injection prevention
- ✅ User isolation

## 📈 Performance

- ✅ Indexed database fields
- ✅ Efficient queries
- ✅ Transaction optimization
- ✅ Connection pooling ready

## ⚙️ Configuration

### Environment Variables
For production, set these environment variables:

```bash
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
DATABASE_URL=postgresql://user:password@host:5432/dbname
```

### Django Settings
Key configuration in `autofare/settings.py`:
- REST_FRAMEWORK authentication
- JWT token settings
- Database configuration
- Static files configuration

## 🐛 Troubleshooting

### "No such table" error
```bash
python manage.py migrate
```

### Port 8000 in use
```bash
python manage.py runserver 8001
```

### Missing dependencies
```bash
pip install -r requirements.txt
```

### Database issues
```bash
python manage.py flush      # Clear database
python manage.py migrate    # Recreate tables
python manage.py shell < sample_data.py  # Load sample data
```

## 🚢 Deployment

### Development
```bash
python manage.py runserver
```

### Production with Gunicorn
```bash
pip install gunicorn
gunicorn autofare.wsgi:application --bind 0.0.0.0:8000
```

### Using Docker
Create a `Dockerfile`:
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "autofare.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## 📝 API Consistency

### Date/Time Format
All timestamps use ISO 8601 format:
```
2026-02-25T14:30:00Z
```

### Currency Format
All amounts use decimal values:
```json
{
  "amount": 99.99
}
```

### Status Codes
```
200 OK              - Successful request
201 Created         - Resource created
400 Bad Request     - Invalid input
404 Not Found       - Resource not found
500 Server Error    - Internal server error
```

## 🔄 Workflow Example

### Complete User Journey

1. **Create User**
   ```bash
   POST /api/users
   ```

2. **Add Vehicle**
   ```bash
   POST /api/user/car
   ```

3. **Add Wallet Funds**
   ```bash
   POST /api/user/wallet
   ```

4. **Capture Toll**
   ```bash
   POST /api/capture/GATE01
   ```

5. **Check Wallet**
   ```bash
   GET /api/user/wallet?user_id=1
   ```

## 📞 Support

For issues or questions:
1. Check [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
2. Review [API_SETUP_GUIDE.md](API_SETUP_GUIDE.md)
3. Check [IMPLEMENTATION_CHECKLIST.md](IMPLEMENTATION_CHECKLIST.md)
4. Run `python verify_setup.py` for system verification

## 📄 Files Reference

### Source Code
- `users/` - User management implementation
- `vehicles/` - Vehicle management implementation
- `toll/` - Toll capture implementation
- `autofare/` - Project configuration

### Testing & Utilities
- `test_api.py` - API test suite
- `sample_data.py` - Sample data generator
- `verify_setup.py` - Environment verification

### Documentation
- `API_DOCUMENTATION.md` - API reference
- `API_SETUP_GUIDE.md` - Setup guide
- `API_TEST_EXAMPLES.http` - Test examples
- `IMPLEMENTATION_CHECKLIST.md` - Verification checklist

## 📋 Requirements

- Python 3.8+
- Django 5.2.7
- Django REST Framework
- Django REST Framework SimpleJWT
- Requests (for testing)

See `requirements.txt` for complete list.

## ✅ Implementation Status

**100% Complete** ✅

All API endpoints have been successfully implemented according to the specification:
- ✅ 9 API endpoints
- ✅ Complete data models
- ✅ Full error handling
- ✅ Comprehensive documentation
- ✅ Test suite included

## 🎓 Learning Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [REST API Best Practices](https://restfulapi.net/)

## 📄 License

This project is part of the Automated Toll Collection System.

---

**Ready to use!** Start with `python manage.py runserver` and refer to[API_DOCUMENTATION.md](API_DOCUMENTATION.md) for additional information.
