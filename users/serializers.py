from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Wallet, Transaction


class UserProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source='user.id', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['user_id', 'name', 'email', 'phone']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['transaction_id', 'amount', 'transaction_type', 'date']
        read_only_fields = ['date']


class WalletSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source='user.id', read_only=True)
    transactions = TransactionSerializer(read_only=True, many=True)
    balance = serializers.DecimalField(source='wallet_balance', max_digits=12, decimal_places=2)
    
    class Meta:
        model = Wallet
        fields = ['user_id', 'balance', 'transactions']


class UserDetailSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(source='profile', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'profile']


class CreateUserSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20)
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email']
        )
        UserProfile.objects.create(
            user=user,
            name=validated_data['name'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            national_id=None
        )
        Wallet.objects.create(user=user)
        return user


class AddFundsSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)


class SignUpSerializer(serializers.Serializer):
    """Serializer for user signup with password registration"""
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20)
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    
    def validate(self, data):
        """Validate that passwords match"""
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return data
    
    def validate_email(self, value):
        """Check if email already exists"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered.")
        return value
    
    def create(self, validated_data):
        """Create user with hashed password"""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=password
        )
        
        UserProfile.objects.create(
            user=user,
            name=validated_data['name'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            national_id=None
        )
        
        Wallet.objects.create(user=user, wallet_balance=0.00)
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for user login with email/password authentication"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        """Validate credentials and return user"""
        email = data.get('email')
        password = data.get('password')
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password.")
        
        if not user.check_password(password):
            raise serializers.ValidationError("Invalid email or password.")
        
        data['user'] = user
        return data
