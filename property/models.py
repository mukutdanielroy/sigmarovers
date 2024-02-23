from django.db import models

from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from user.models import CustomUser

# Create your models here.
class PropertyType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "Property Types"

class PropertyTypeCategory(models.Model):
    property_type = models.ForeignKey(PropertyType, related_name='property_types', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"Property type: {self.property_type.name}, category: {self.name}"

    class Meta:
        verbose_name_plural = "Property Type Categories"

STATUS_CHOICES = (
    ('Ready', 'Ready'),
    ('Off-Plan', 'Off-Plan'),
)

class Location(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"

class Amenity(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name_plural = "Amenities"


class AddOn(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name_plural = "Add-on Services"

class Bed(models.Model):
    number = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.number}"

class Bath(models.Model):
    number = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.number}"

class Property(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    bedrooms = models.IntegerField()
    beds = models.ForeignKey(Bed, on_delete=models.CASCADE)
    baths = models.ForeignKey(Bath, on_delete=models.CASCADE)
    area_sqft = models.IntegerField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    google_map_location = models.CharField(max_length=255, blank=True)
    available = models.BooleanField(default=False)
    property_type = models.ForeignKey(PropertyType, on_delete=models.CASCADE)
    property_type_category = models.ForeignKey(PropertyTypeCategory, on_delete=models.CASCADE)
    amenities = models.ManyToManyField(Amenity, blank=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name_plural = "Properties"

class BuyProperty(Property):
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    price = models.IntegerField()

    def __str__(self):
        return f"Title for Property: {self.title}"

    class Meta:
        verbose_name_plural = "Buy Properties"

class RentProperty(Property):
    total_guests = models.IntegerField()
    price_daily = models.IntegerField()
    weekly_discount_percent = models.IntegerField(default=None, null=True, blank=True)
    monthly_discount_percent = models.IntegerField(default=None, null=True, blank=True)
    yearly_discount_percent = models.IntegerField(default=None, null=True, blank=True)
    addons = models.ManyToManyField(AddOn, blank=True)

    def __str__(self):
        return f"{self.title}"
    
    def weekly_price(self):
        if self.weekly_discount_percent is not None:
            weekly_price = self.price_daily * 7 * (1 - self.weekly_discount_percent / 100)
        else:
            weekly_price = self.price_daily * 7
        return int(weekly_price)

    def monthly_price(self):
        if self.monthly_discount_percent is not None:
            monthly_price = self.price_daily * 30 * (1 - self.monthly_discount_percent / 100)
        else:
            monthly_price = self.price_daily * 30
        return int(monthly_price)

    def yearly_price(self):
        if self.yearly_discount_percent is not None:
            yearly_price = self.price_daily * 365 * (1 - self.yearly_discount_percent / 100)
        else:
            yearly_price = self.price_daily * 365
        return int(yearly_price)

    class Meta:
        verbose_name_plural = "Rent Properties"

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, related_name='property_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_images/')

    def __str__(self):
        return f"{self.property.title}"
    
    class Meta:
        verbose_name_plural = "Property Images"

class Review(models.Model):
    property = models.ForeignKey(Property, related_name='property_reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by: {self.user.username} for the Property: {self.property.title}"

class Booking(models.Model):
    property = models.ForeignKey(RentProperty, related_name='rent_property_bookings', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    check_in_date = models.DateField(default=timezone.now)
    check_out_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.user}'s booking for {self.property} from {self.check_in_date} to {self.check_out_date}"

class Wishlist(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='wishlists')
    properties = models.ManyToManyField(Property)

    def __str__(self):
        return f"Wishlist for {self.user.username}"