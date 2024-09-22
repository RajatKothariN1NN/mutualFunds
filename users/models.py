from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, phone_number, PAN, password=None, **extra_fields):
        required_fields = {
            'email': email,
            'phone_number': phone_number,
            'PAN': PAN
        }

        for field_name, value in required_fields.items():
            if not value:
                raise ValueError(f'The {field_name.replace("_", " ").capitalize()} field must be set')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            phone_number=phone_number,
            PAN=PAN,
            **extra_fields
        )
        user.set_password(password) # Hashes the password
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, phone_number, PAN, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, phone_number, PAN, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # Updated to use ImageField
    PAN = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = CustomUserManager()
    class Meta:
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['username'])

        ]
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number', 'PAN']


    def __str__(self):
        return self.email.split('@')[0]


class UserPreferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # One-to-one relationship with User
    fund_types = models.JSONField(default=list)  # Stores fund types as a JSON list
    risk_profiles = models.JSONField(default=list)  # Stores risk profiles as a JSON list
    themes = models.JSONField(default=list)  # Stores themes as a JSON list
    investment_duration = models.CharField(max_length=100, blank=True)  # Stores investment duration as a string
    expected_returns = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Stores expected returns

    class Meta:
        indexes = [
            models.Index(fields=['user']),

        ]
    def __str__(self):
        return f"{self.user.username}'s Preferences"
