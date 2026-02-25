"""
Sample data initialization script for the Automated Toll Collection System.
This script creates sample users, vehicles, gates, and tolls for testing the API.

Run with: python manage.py shell < sample_data.py
"""

from django.contrib.auth.models import User
from users.models import UserProfile, Wallet, Transaction
from vehicles.models import Vehicle
from toll.models import Gate, Toll, Trip
from decimal import Decimal
from django.utils import timezone

# Clear existing data (optional)
# User.objects.all().delete()
# Gate.objects.all().delete()
# Toll.objects.all().delete()

# Create sample users
print("Creating sample users...")
user1, created = User.objects.get_or_create(
    username='john@example.com',
    defaults={
        'email': 'john@example.com',
        'first_name': 'John',
        'last_name': 'Doe'
    }
)

if created:
    UserProfile.objects.create(
        user=user1,
        name='John Doe',
        email='john@example.com',
        phone='1234567890',
        national_id='JD12345'
    )
    Wallet.objects.create(user=user1, wallet_balance=Decimal('1000.00'))
    print(f"Created user: {user1.username}")
else:
    print(f"User already exists: {user1.username}")

user2, created = User.objects.get_or_create(
    username='jane@example.com',
    defaults={
        'email': 'jane@example.com',
        'first_name': 'Jane',
        'last_name': 'Smith'
    }
)

if created:
    UserProfile.objects.create(
        user=user2,
        name='Jane Smith',
        email='jane@example.com',
        phone='0987654321',
        national_id='JS54321'
    )
    Wallet.objects.create(user=user2, wallet_balance=Decimal('500.00'))
    print(f"Created user: {user2.username}")
else:
    print(f"User already exists: {user2.username}")

# Create sample vehicles
print("\nCreating sample vehicles...")
vehicle1, created = Vehicle.objects.get_or_create(
    license_plate='XYZ-987',
    defaults={
        'user': user1,
        'vehicle_type': 'car',
        'vehicle_model': 'Toyota Camry',
        'vehicle_color': 'Blue'
    }
)
if created:
    print(f"Created vehicle: {vehicle1.license_plate}")
else:
    print(f"Vehicle already exists: {vehicle1.license_plate}")

vehicle2, created = Vehicle.objects.get_or_create(
    license_plate='ABC-123',
    defaults={
        'user': user2,
        'vehicle_type': 'truck',
        'vehicle_model': 'Volvo FH16',
        'vehicle_color': 'Red'
    }
)
if created:
    print(f"Created vehicle: {vehicle2.license_plate}")
else:
    print(f"Vehicle already exists: {vehicle2.license_plate}")

# Create sample tolls
print("\nCreating sample tolls...")
toll_car, created = Toll.objects.get_or_create(
    toll_id='TOLL_CAR',
    defaults={'amount': Decimal('5.50')}
)
if created:
    print(f"Created toll: {toll_car.toll_id} - ${toll_car.amount}")

toll_truck, created = Toll.objects.get_or_create(
    toll_id='TOLL_TRUCK',
    defaults={'amount': Decimal('10.00')}
)
if created:
    print(f"Created toll: {toll_truck.toll_id} - ${toll_truck.amount}")

# Create sample gates
print("\nCreating sample gates...")
gate1, created = Gate.objects.get_or_create(
    gate_id='GATE01',
    defaults={
        'gate_name': 'Main Toll Gate',
        'gate_location': 'Highway 5 North'
    }
)
if created:
    gate1.tolls.add(toll_car, toll_truck)
    print(f"Created gate: {gate1.gate_id} - {gate1.gate_name}")
else:
    print(f"Gate already exists: {gate1.gate_id}")

gate2, created = Gate.objects.get_or_create(
    gate_id='GATE02',
    defaults={
        'gate_name': 'Secondary Toll Gate',
        'gate_location': 'Highway 5 South'
    }
)
if created:
    gate2.tolls.add(toll_car, toll_truck)
    print(f"Created gate: {gate2.gate_id} - {gate2.gate_name}")
else:
    print(f"Gate already exists: {gate2.gate_id}")

print("\nSample data initialization completed!")
print("\nYou can now test the API endpoints:")
print("- Create User: POST /api/users")
print("- List Users: GET /api/users")
print("- Add Vehicle: POST /api/user/car")
print("- List Vehicles: GET /api/user/car")
print("- Get Wallet: GET /api/user/wallet?user_id=1")
print("- Add Funds: POST /api/user/wallet")
print("- Capture Toll: POST /api/capture/GATE01")
