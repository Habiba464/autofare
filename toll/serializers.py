from rest_framework import serializers
from .models import Trip, Gate
from vehicles.models import Vehicle


class TollCaptureSerializer(serializers.Serializer):
    license_plate = serializers.CharField(max_length=20)
    
    def validate_license_plate(self, value):
        try:
            Vehicle.objects.get(license_plate=value)
        except Vehicle.DoesNotExist:
            raise serializers.ValidationError("Vehicle with this license plate not found.")
        return value


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ['trip_id', 'vehicle', 'gate', 'trip_time', 'fare_amount', 'status']
        read_only_fields = ['trip_time', 'fare_amount']
