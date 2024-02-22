from rest_framework import serializers
from .models import Property, PropertyType, PropertyTypeCategory, BuyProperty, Location, Amenity, PropertyImage, Review, RentProperty, Booking, AddOn, Bed, Bath

# Used for now
from django.contrib.auth.models import User

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'

class PropertyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyType
        fields = '__all__'

class PropertyTypeCategorySerializer(serializers.ModelSerializer):
    property_type = PropertyTypeSerializer()

    class Meta:
        model = PropertyTypeCategory
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = '__all__'

class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['image']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class BedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bed
        fields = '__all__'

class BathSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bath
        fields = '__all__'

class BuyPropertySerializer(serializers.ModelSerializer):
    beds = BedSerializer()
    baths = BathSerializer()
    location = LocationSerializer()
    amenities = AmenitySerializer(many=True)
    property_type = PropertyTypeSerializer()
    property_type_category = PropertyTypeCategorySerializer()
    property_images = PropertyImageSerializer(many=True)
    property_reviews = ReviewSerializer(many=True)

    class Meta:
        model = BuyProperty
        fields = '__all__'

class AddOnSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddOn
        fields = '__all__'

class BookingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

class RentPropertySerializer(serializers.ModelSerializer):
    beds = BedSerializer()
    baths = BathSerializer()
    location = LocationSerializer()
    amenities = AmenitySerializer(many=True)
    property_type = PropertyTypeSerializer()
    property_type_category = PropertyTypeCategorySerializer()
    property_images = PropertyImageSerializer(many=True)
    property_reviews = ReviewSerializer(many=True)
    addons = AddOnSerializer(many=True)
    rent_property_bookings = BookingsSerializer(many=True)

    weekly_price = serializers.IntegerField(read_only=True)
    monthly_price = serializers.IntegerField(read_only=True)
    yearly_price = serializers.IntegerField(read_only=True)

    class Meta:
        model = RentProperty
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    property = RentPropertySerializer()

    class Meta:
        model = Booking
        fields = '__all__'