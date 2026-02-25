from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import UserProfile, Wallet, Transaction
from .serializers import (
    UserProfileSerializer,
    WalletSerializer,
    CreateUserSerializer,
    AddFundsSerializer,
    TransactionSerializer,
    SignUpSerializer,
    LoginSerializer
)
from django.db import transaction
from django.utils import timezone


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUserSerializer
        return UserProfileSerializer
    
    def list(self, request, *args, **kwargs):
        """GET /users - Retrieve all registered user data"""
        users = User.objects.all()
        data = []
        for user in users:
            try:
                profile = user.profile
                data.append({
                    "user_id": str(user.id),
                    "name": profile.name,
                    "email": profile.email,
                    "phone": profile.phone
                })
            except UserProfile.DoesNotExist:
                continue
        return Response(data)
    
    def create(self, request, *args, **kwargs):
        """POST /users - Add a new user to the system"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "message": "User added successfully",
                "user_id": str(user.id)
            },
            status=status.HTTP_201_CREATED
        )
    
    def destroy(self, request, *args, **kwargs):
        """DELETE /users/{user_id} - Remove a user from the system"""
        user = self.get_object()
        user.delete()
        return Response(
            {"message": "User deleted successfully"},
            status=status.HTTP_200_OK
        )


class WalletViewSet(viewsets.ViewSet):
    """Wallet endpoints for balance and transaction history"""
    
    def list(self, request):
        """GET /user/wallet - Retrieve wallet balance and transaction history"""
        user_id = request.query_params.get('user_id')
        
        if not user_id:
            return Response(
                {"error": "user_id query parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(id=user_id)
            wallet = user.wallet
        except (User.DoesNotExist, Wallet.DoesNotExist):
            return Response(
                {"error": "User or wallet not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)
    
    def create(self, request):
        """POST /user/wallet - Add money to the user's wallet"""
        serializer = AddFundsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user_id = serializer.validated_data['user_id']
        amount = serializer.validated_data['amount']
        
        try:
            user = User.objects.get(id=user_id)
            wallet = user.wallet
        except (User.DoesNotExist, Wallet.DoesNotExist):
            return Response(
                {"error": "User or wallet not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        with transaction.atomic():
            wallet.wallet_balance += amount
            wallet.save()
            
            # Create transaction record
            Transaction.objects.create(
                wallet=wallet,
                transaction_id=f"TXN{timezone.now().timestamp()}",
                transaction_type="top-up",
                amount=amount
            )
        
        return Response(
            {
                "message": "Wallet updated successfully",
                "new_balance": float(wallet.wallet_balance)
            },
            status=status.HTTP_200_OK
        )


class AuthViewSet(viewsets.ViewSet):
    """Authentication endpoints for signup and login"""
    
    @action(detail=False, methods=['post'])
    def signup(self, request):
        """POST /api/auth/signup - User registration with password"""
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response(
            {
                "message": "User registered successfully",
                "user_id": str(user.id),
                "email": user.email,
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            },
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        """POST /api/auth/login - User authentication with JWT tokens"""
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        profile = user.profile
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response(
            {
                "message": "Login successful",
                "user_id": str(user.id),
                "name": profile.name,
                "email": profile.email,
                "phone": profile.phone,
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            },
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['post'])
    def refresh_token(self, request):
        """POST /api/auth/refresh_token - Refresh access token using refresh token"""
        refresh_token = request.data.get('refresh')
        
        if not refresh_token:
            return Response(
                {"error": "Refresh token is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            refresh = RefreshToken(refresh_token)
            return Response(
                {
                    "message": "Token refreshed successfully",
                    "access": str(refresh.access_token)
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": "Invalid refresh token"},
                status=status.HTTP_400_BAD_REQUEST
            )
