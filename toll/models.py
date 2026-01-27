from django.db import models
from django.conf import settings

class Toll(models.Model):
    toll_id = models.CharField(max_length=50, primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

class Gate(models.Model):
    gate_id = models.CharField(max_length=50, primary_key=True)
    gate_name = models.CharField(max_length=100)
    gate_location = models.CharField(max_length=255)
    tolls = models.ManyToManyField(Toll, related_name='gates') # "belongs" relationship

class Trip(models.Model):
    trip_id = models.AutoField(primary_key=True)
    vehicle = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gate = models.ForeignKey(Gate, on_delete=models.CASCADE)
    trip_time = models.DateTimeField(auto_now_add=True)
    fare_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='Pending') # Paid, Unpaid