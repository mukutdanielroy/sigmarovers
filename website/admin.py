from django.contrib import admin, messages

from .models import NavMenu, SocialMedia
from django.core.exceptions import ValidationError

# Register your models here.

def make_active_nav_menu(modeladmin, request, queryset):
    total_active_menu = NavMenu.total_active_menu
    active_count = NavMenu.objects.filter(active=True).count()
    if active_count + queryset.count() > total_active_menu:
        modeladmin.message_user(request, ("Number of active items exceeds the limit."), level=messages.ERROR)
    else:
        queryset.update(active=True)
make_active_nav_menu.short_description = "Activate selected items"

def make_deactive(modeladmin, request, queryset):
    queryset.update(active=False)
make_deactive.short_description = "Deactivate selected items"

class NavMenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'serial', 'active', 'url', 'total_active_menu')
    actions = [make_active_nav_menu, make_deactive]
    
    def save_model(self, request, obj, form, change):
        try:
            if obj.active:
                active_count = NavMenu.objects.filter(active=True).exclude(pk=obj.pk).count()
                if active_count >= obj.total_active_menu:
                    raise ValidationError(f"Total active menu not be more than {obj.total_active_menu}")
        except ValidationError as e:
            for message in e.messages:
                self.message_user(request, message, level=messages.ERROR)
            return
        else:
            super().save_model(request, obj, form, change)

def make_active_social_media(modeladmin, request, queryset):
    total_active_social_media = SocialMedia.total_active_social_media
    active_count = SocialMedia.objects.filter(active=True).count()
    if active_count + queryset.count() > total_active_social_media:
        modeladmin.message_user(request, ("Number of active items exceeds the limit."), level=messages.ERROR)
    else:
        queryset.update(active=True)
make_active_social_media.short_description = "Activate selected items"

class SocialNetworkAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'serial', 'active', 'url', 'total_active_social_media')
    actions = [make_active_social_media, make_deactive]

    def save_model(self, request, obj, form, change):
        try:
            if obj.active:
                active_count = SocialMedia.objects.filter(active=True).exclude(pk=obj.pk).count()
                if active_count >= obj.total_active_social_media:
                    raise ValidationError(f"Total social mediashould not be more than {obj.total_active_social_media}")
        except ValidationError as e:
            for message in e.messages:
                self.message_user(request, message, level=messages.ERROR)
            return
        else:
            super().save_model(request, obj, form, change)

admin.site.register(NavMenu, NavMenuAdmin)
admin.site.register(SocialMedia, SocialNetworkAdmin)