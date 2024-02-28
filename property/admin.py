from django.contrib import admin
from .models import PropertyType, PropertyTypeCategory, Property, PropertyImage, Location, Amenity, AddOn, Review, Wishlist, BuyProperty, RentProperty, Booking, Bed, Bath, Agency
from django.utils.html import mark_safe
from django.urls import reverse

# Register your models here.

class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ['name']

class PropertyTypeCategoryAdmin(admin.ModelAdmin):
    list_display = ['property_type', 'name']

class LocationAdmin(admin.ModelAdmin):
    list_display = ['name']

class AmenityAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon']

class AddOnAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon']

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1
    readonly_fields = ['image_tag']

    def image_tag(self, obj):
        if obj.image:
            return mark_safe('<img src="{}" style="max-height: 200px; max-width: 200px;" />'.format(obj.image.url))
        else:
            return None
    image_tag.short_description = 'Actual Image'

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1

class BuyPropertyAdmin(admin.ModelAdmin):
    inlines = [PropertyImageInline, ReviewInline]
    list_display = ['title', 'contact_person', 'price', 'status', 'bedrooms', 'beds', 'baths', 'area_sqft', 'location', 'property_type', 'property_type_category', 'available']
    list_filter = ['status', 'available']
    search_fields = ['title', 'description', 'location__name']
    readonly_fields = ('created_at',)

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'contact_person', 'price', 'status', 'bedrooms', 'beds', 'baths', 'area_sqft', 'location', 'google_map_location', 'available', 'agency')
        }),
        ('Property Details', {
            'fields': ('property_type', 'property_type_category', 'amenities', 'created_at')
        }),
    )

    filter_horizontal = ['amenities']

class RentPropertyAdmin(admin.ModelAdmin):
    inlines = [PropertyImageInline, ReviewInline]
    list_display = ['title', 'contact_person', 'total_guests', 'price_daily', 'weekly_price', 'monthly_price', 'yearly_price', 'weekly_discount_percent', 'monthly_discount_percent', 'yearly_discount_percent', 'bedrooms', 'beds', 'baths', 'area_sqft', 'location', 'property_type', 'property_type_category', 'available']
    list_filter = ['available']
    search_fields = ['title', 'description', 'location__name']
    readonly_fields = ('created_at',)

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'contact_person', 'total_guests', 'bedrooms', 'beds', 'baths', 'area_sqft', 'location', 'google_map_location', 'available')
        }),
        ('Price Details', {
            'fields': ('price_daily', 'weekly_discount_percent', 'monthly_discount_percent', 'yearly_discount_percent')
        }),
        ('Property Details', {
            'fields': ('property_type', 'property_type_category', 'amenities', 'addons', 'created_at')
        }),
    )

    filter_horizontal = ['amenities', 'addons']

class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ['image_tag', 'property']
    readonly_fields = ['image_tag']

    def image_tag(self, obj):
        if obj.image:
            return mark_safe('<img src="{}" style="max-height: 200px; max-width: 200px;" />'.format(obj.image.url))
        else:
            return None
    image_tag.short_description = 'Actual Image'

class PropertyAdmin(admin.ModelAdmin):
    inlines = [PropertyImageInline, ReviewInline]
    list_display = list_display = ['title', 'contact_person', 'bedrooms', 'beds', 'baths', 'area_sqft', 'location', 'available', 'property_type', 'property_type_category']
    search_fields = ['title', 'description', 'location__name']
    actions = None  # Disable all actions

    def has_add_permission(self, request):
        return False  # Disable the add action

    def has_change_permission(self, request, obj=None):
        return False  # Disable the change action

    def has_delete_permission(self, request, obj=None):
        return False  # Disable the delete action

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        rent_property_ids = RentProperty.objects.values_list('id', flat=True)
        buy_property_ids = BuyProperty.objects.values_list('id', flat=True)
        queryset = Property.objects.filter(id__in=rent_property_ids) | Property.objects.filter(id__in=buy_property_ids)
        print(queryset)
        return queryset.distinct()

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['property', 'user', 'rating', 'created_at']
    list_filter = ['property', 'user', 'rating']
    search_fields = ['property__title', 'comment']
    readonly_fields = ['created_at']

class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'display_properties']
    filter_horizontal = ['properties']
    readonly_fields = ('created_at',)

    def display_properties(self, obj):
        properties_html = ''
        for property in obj.properties.all():
            property_url = reverse('admin:property_property_change', args=[property.id])
            properties_html += f'<p><a href="{property_url}">{property.title}</a></p>'
        return mark_safe(properties_html)

    display_properties.short_description = 'Properties'

class BookingAdmin(admin.ModelAdmin):
    list_display = ['property', 'user', 'check_in_date', 'check_out_date']
    list_filter = ['property', 'user', 'check_in_date', 'check_out_date']
    search_fields = ['property__title',]
    date_hierarchy = 'check_in_date'
    readonly_fields = ('created_at',)

admin.site.register(PropertyType, PropertyTypeAdmin)
admin.site.register(PropertyTypeCategory, PropertyTypeCategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Amenity, AmenityAdmin)
admin.site.register(AddOn, AddOnAdmin)
admin.site.register(BuyProperty, BuyPropertyAdmin)
admin.site.register(RentProperty, RentPropertyAdmin)
admin.site.register(PropertyImage, PropertyImageAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Bed)
admin.site.register(Bath)
admin.site.register(Agency)