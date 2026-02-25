from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db import transaction
from .models import Gate, Trip, Toll
from .serializers import TollCaptureSerializer, TripSerializer
from vehicles.models import Vehicle
from users.models import Wallet, Transaction


class TollCaptureViewSet(viewsets.ViewSet):
    """Toll Capture endpoints for gate processing"""
    
    @action(detail=False, methods=['post'], url_path='capture/(?P<gate_id>[^/.]+)')
    def capture_vehicle(self, request, gate_id=None):
        """POST /capture/{gate_id} - Capture vehicle at toll gate"""
        if not gate_id:
            return Response(
                {"error": "gate_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = TollCaptureSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        license_plate = serializer.validated_data['license_plate']
        
        try:
            gate = Gate.objects.get(gate_id=gate_id)
        except Gate.DoesNotExist:
            return Response(
                {"error": f"Gate {gate_id} not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            vehicle = Vehicle.objects.get(license_plate=license_plate)
        except Vehicle.DoesNotExist:
            return Response(
                {"error": "Vehicle not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        user = vehicle.user
        
        with transaction.atomic():
            # Create trip record
            trip = Trip.objects.create(
                vehicle=vehicle,
                gate=gate,
                status='pending'
            )
            
            # Get toll amount
            toll = gate.tolls.first()
            toll_amount = toll.amount if toll else 5.50
            
            # Process payment
            try:
                wallet = user.wallet
                if wallet.wallet_balance >= toll_amount:
                    wallet.wallet_balance -= toll_amount
                    wallet.save()
                    trip.status = 'paid'
                    trip.fare_amount = toll_amount
                else:
                    trip.status = 'unpaid'
                    trip.fare_amount = toll_amount
                
                trip.save()
                
                # Create transaction record
                Transaction.objects.create(
                    wallet=wallet,
                    transaction_id=f"TXN{timezone.now().timestamp()}",
                    transaction_type="toll-charge",
                    amount=toll_amount
                )
            except Wallet.DoesNotExist:
                trip.status = 'unpaid'
                trip.fare_amount = toll_amount
                trip.save()
        
        return Response(
            {
                "message": "Toll captured successfully",
                "user_id": str(user.id),
                "amount_charged": float(trip.fare_amount),
                "location": f"{gate.gate_name} - {gate.gate_location}",
                "timestamp": trip.trip_time.isoformat()
            },
            status=status.HTTP_200_OK
        )
