from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

class GovernmentID(models.Model):
    ID_TYPE_CHOICES = [
        ('DL', 'Driving License'),
        ('PP', 'Passport'),
        ('ID', 'Identity Card'),
    ]

    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE)
    id_type = models.CharField(max_length=2, choices=ID_TYPE_CHOICES)
    id_photo = models.ImageField(upload_to='government_id_photos/')

    class Meta:
        verbose_name_plural = "Government IDs"

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    legal_name = models.CharField(max_length=255, blank=True)
    government_id = models.OneToOneField(GovernmentID, on_delete=models.SET_NULL, null=True, blank=True)
    verified = models.BooleanField(default=False)
    address = models.TextField(blank=True)
    emergency_contact_name = models.CharField(max_length=255, blank=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True)
    emergency_contact_address = models.CharField(max_length=15, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Add your custom fields here

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name_plural = "Users"
