from rest_framework import serializers
from .models import UserHealth,ConstomUser
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password

User = get_user_model()
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            phone=validated_data['phone']
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()

    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid email or password")
        
        return {'user': user}


class UserProfileSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True, required=False, min_length=8, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=False, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone', 'address', 'new_password', 'confirm_password']
        read_only_fields = ['email']

    def validate(self, data):
        # Ensure both new_password and confirm_password match
        if 'new_password' in data and 'confirm_password' in data:
            if data['new_password'] != data['confirm_password']:
                raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return data

    def update(self, instance, validated_data):
        # Update user fields
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.address = validated_data.get('address', instance.address)

        # Handle password change
        new_password = validated_data.get('new_password', None)
        if new_password:
            instance.set_password(new_password)

        instance.save()
        return instance

class UserHealthSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=ConstomUser.objects.all())

    class Meta:
        model = UserHealth
        fields = ['user', 'age', 'weight', 'daily_calorie_limit']

