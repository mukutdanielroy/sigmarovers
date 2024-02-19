from django.db import models

# Create your models here.

class NavMenu(models.Model):
    name = models.CharField(max_length=100)
    serial = models.IntegerField(unique=True)
    active = models.BooleanField(default=False)
    url = models.CharField(max_length=100, default='#')

    total_active_menu = 5

    def __str__(self):
        return f"{self.name}"

class SocialMedia(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50)
    serial = models.IntegerField(unique=True)
    active = models.BooleanField(default=False)
    url = models.CharField(max_length=100, default='#')

    total_active_social_media = 5

    def __str__(self):
        return f"{self.name}"