from rest_framework import serializers

from funds.models import FundType, RiskProfile
from .models import User, UserPreferences


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)  # Handle password update separately
    profile_pic = serializers.ImageField(required=False)  # Allow image upload
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)
    PAN = serializers.CharField(required=False)  # Updated to allow image upload
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'profile_pic', 'PAN', 'phone_number', 'is_staff', 'is_superuser']

    def validate_username(self, value):
        # For registration, check uniqueness. For update, only check if the username is being changed.
        if self.instance is None:  # This is a registration
            if User.objects.filter(username=value).exists():
                raise serializers.ValidationError("A user with this username already exists.")
        else:  # This is an update
            if value != self.instance.username and User.objects.filter(username=value).exists():
                raise serializers.ValidationError("A user with this username already exists.")
        return value

    def validate_email(self, value):
        # For registration, check uniqueness. For update, only check if the email is being changed.
        if self.instance is None:  # This is a registration
            if User.objects.filter(email=value).exists():
                raise serializers.ValidationError("A user with this email already exists.")
        else:  # This is an update
            if value != self.instance.email and User.objects.filter(email=value).exists():
                raise serializers.ValidationError("A user with this email already exists.")
        return value


    def update(self, instance, validated_data):
        profile_pic = validated_data.pop('profile_pic', None)
        if profile_pic:
            instance.profile_pic = profile_pic

        # Update other fields
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.PAN = validated_data.get('PAN', instance.PAN)

        instance.save()
        return instance

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


class UserPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreferences
        fields = ['fund_types', 'risk_profiles', 'themes', 'investment_duration', 'expected_returns']
