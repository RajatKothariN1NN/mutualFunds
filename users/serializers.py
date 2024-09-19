from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Ensure password is write-only
    profile_pic = serializers.ImageField(required=False)  # Updated to allow image upload
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'profile_pic', 'PAN', 'phone_number', 'is_staff', 'is_superuser']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],  # Handle password
            profile_pic=validated_data.get('profile_pic'),
            PAN=validated_data.get('PAN'),
            phone_number=validated_data.get('phone_number')
        )
        return user
