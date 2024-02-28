from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
import os
from datetime import datetime

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

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    mobile = models.CharField(max_length=20, unique=True, null=True, blank=True)
    legal_name = models.CharField(max_length=255, null=True, blank=True)
    verified = models.BooleanField(default=False)
    address = models.TextField(null=True, blank=True)
    emergency_contact_mobile = models.CharField(max_length=20, null=True, blank=True)
    emergency_contact_address = models.CharField(max_length=255, null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    whatsapp = models.CharField(max_length=20, unique=True, null=True, blank=True)

    # Add your custom fields here

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name_plural = "Users"

class GovernmentID(models.Model):
    ID_TYPE_CHOICES = [
        ('DL', 'Driving License'),
        ('PP', 'Passport'),
        ('ID', 'Identity Card'),
    ]

    user = models.ForeignKey(CustomUser, related_name='government_ids', on_delete=models.CASCADE)
    id_type = models.CharField(max_length=2, choices=ID_TYPE_CHOICES)
    id_photo_front = models.ImageField(upload_to='government_id_photos/',)
    id_photo_back = models.ImageField(upload_to='government_id_photos/', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Government IDs"
    
    def __str__(self):
        return f'{self.user.username}'
    
    def save(self, *args, **kwargs):
        # Get original filenames
        front_filename = os.path.basename(self.id_photo_front.name)
        back_filename = os.path.basename(self.id_photo_back.name) if self.id_photo_back else None


        current_date = datetime.now()
        date_string = current_date.strftime('%Y%m%d')

        # Construct new filenames
        new_front_filename = f"{self.user.id}_{self.user.username}_{date_string}_front_{front_filename}"
        new_back_filename = f"{self.user.id}_{self.user.username}_{date_string}_back_{back_filename}" if back_filename else None

        # Set new filenames
        self.id_photo_front.name = new_front_filename
        if self.id_photo_back:
            self.id_photo_back.name = new_back_filename

        super().save(*args, **kwargs)