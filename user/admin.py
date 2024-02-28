from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, GovernmentID
from django.utils.html import format_html
from django.conf import settings

class GovernmentIDInline(admin.StackedInline):
    model = GovernmentID
    extra = 1

class CustomUserAdmin(UserAdmin):
    inlines = [GovernmentIDInline]
    list_display = ('email', 'username', 'mobile', 'legal_name', 'verified', 'date_joined')
    search_fields = ('email', 'username', 'mobile')
    readonly_fields = ('date_joined', 'last_login')

    fieldsets = (
        (None, {
            'fields': ('email', 'username', 'password', 'verified')
        }),
        ('Personal info', {
            'classes': ['collapse'],
            'fields': ('legal_name', 'mobile', 'address', 'emergency_contact_mobile', 'emergency_contact_address', 'whatsapp')
        }),
        ('Permissions', {
            'classes': ['collapse'],
            'fields': ('is_active', 'is_staff', 'groups', 'user_permissions')
        }),
        ('Important dates', {
            'classes': ['collapse'],
            'fields': ('date_joined', 'last_login')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'verified'),
        }),
        ('Personal info', {
            'classes': ['collapse'],
            'fields': ('legal_name', 'mobile', 'address', 'emergency_contact_mobile', 'emergency_contact_address', 'whatsapp')
        }),
        ('Permissions', {
            'classes': ['collapse'],
            'fields': ('is_active', 'is_staff', 'groups', 'user_permissions')
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(GovernmentID)
