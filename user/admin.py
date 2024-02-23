from django.contrib import admin
from .models import CustomUser, GovernmentID

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(GovernmentID)