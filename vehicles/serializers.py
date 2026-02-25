from rest_framework import serializers
from .models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    car_id = serializers.CharField(source='id', read_only=True)
    user_id = serializers.CharField(source='user.id', read_only=True)
    model = serializers.CharField(source='vehicle_model')
    color = serializers.CharField(source='vehicle_color')
    
    class Meta:
        model = Vehicle
        fields = ['car_id', 'user_id', 'license_plate', 'model', 'color', 'vehicle_type']
        read_only_fields = ['car_id', 'user_id']


class CreateVehicleSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    model = serializers.CharField(source='vehicle_model')
    color = serializers.CharField(source='vehicle_color')
    
    class Meta:
        model = Vehicle
        fields = ['user_id', 'license_plate', 'model', 'color', 'vehicle_type']
    
    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        from django.contrib.auth.models import User
        user = User.objects.get(id=user_id)
        vehicle = Vehicle.objects.create(user=user, **validated_data)
        return vehicle
