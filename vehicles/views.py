from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Vehicle
from .serializers import VehicleSerializer, CreateVehicleSerializer


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CreateVehicleSerializer
        return VehicleSerializer
    
    def list(self, request, *args, **kwargs):
        """GET /user/car - Retrieve vehicle data for all users or a specific user"""
        user_id = request.query_params.get('user_id')
        
        if user_id:
            vehicles = Vehicle.objects.filter(user_id=user_id)
        else:
            vehicles = Vehicle.objects.all()
        
        serializer = VehicleSerializer(vehicles, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """POST /user/car - Add vehicle information for a user"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        vehicle = serializer.save()
        
        return Response(
            {
                "message": "Vehicle added successfully",
                "car_id": str(vehicle.id)
            },
            status=status.HTTP_201_CREATED
        )
    
    def destroy(self, request, *args, **kwargs):
        """DELETE /user/car/{car_id} - Remove a vehicle from the system"""
        vehicle = self.get_object()
        vehicle.delete()
        return Response(
            {"message": "Vehicle deleted successfully"},
            status=status.HTTP_200_OK
        )
