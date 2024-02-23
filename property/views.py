from rest_framework import generics
from .models import PropertyTypeCategory, BuyProperty, RentProperty, Booking, Property
from .serializers import PropertyTypeCategorySerializer, BuyPropertySerializer, RentPropertySerializer, BookingSerializer, PropertySerializer
from rest_framework import viewsets
from django.db.models import Q

# Create your views here.

class PropertyTypeCategoryViewSet(viewsets.ModelViewSet):
    queryset = PropertyTypeCategory.objects.all()
    serializer_class = PropertyTypeCategorySerializer

class BuyPropertyListAPIView(generics.ListAPIView):
    queryset = BuyProperty.objects.all()
    serializer_class = BuyPropertySerializer

class BuyPropertyDetailAPIView(generics.RetrieveAPIView):
    queryset = BuyProperty.objects.all()
    serializer_class = BuyPropertySerializer

class RentPropertyListAPIView(generics.ListAPIView):
    queryset = RentProperty.objects.all()
    serializer_class = RentPropertySerializer

class RentPropertyDetailAPIView(generics.RetrieveAPIView):
    queryset = RentProperty.objects.all()
    serializer_class = RentPropertySerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class BookingListAPIView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class BookingDetailAPIView(generics.RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    
class PropertySearchAPIView(generics.ListAPIView):
    serializer_class = PropertySerializer

    def get_queryset(self):
        # Retrieve the 'location' query parameter from the request
        purpose = self.request.query_params.get('purpose', None)
        beds = self.request.query_params.get('beds', None)
        baths = self.request.query_params.get('baths', None)
        area_sqft_min = self.request.query_params.get('area_sqft_min', None)
        area_sqft_max = self.request.query_params.get('area_sqft_max', None)
        location = self.request.query_params.get('location', None)
        property_type = self.request.query_params.get('property_type', None)
        property_type_category = self.request.query_params.get('property_type_category', None)
        queryset = None
        filters = Q()
        if location:
            filters &= Q(location__id__icontains=location)
        if property_type:
            filters &= Q(property_type__id=property_type)
        if property_type_category:
            filters &= Q(property_type_category__id=property_type_category)
        if beds:
            filters &= Q(beds__id=beds)
        if baths:
            filters &= Q(baths__id=baths)
        if area_sqft_min:
            filters &= Q(area_sqft__gte=area_sqft_min)
        if area_sqft_max:
            filters &= Q(area_sqft__lte=area_sqft_max)
        if purpose.lower() == 'rent':
            self.serializer_class = RentPropertySerializer
            price_frequency = self.request.query_params.get('price_frequency', None)
            price_min = self.request.query_params.get('price_min', None)
            price_max = self.request.query_params.get('price_max', None)
            if price_frequency == 'weekly':
                filters &= Q(weekly_discount_percent__isnull=False)
            if price_frequency == 'monthly':
                filters &= Q(monthly_discount_percent__isnull=False)
            if price_frequency == 'yearly':
                filters &= Q(yearly_discount_percent__isnull=False)
            if price_min:
                filters &= Q(price_daily__gte=price_min)
            if price_max:
                filters &= Q(price_daily__lte=price_max)
            if price_frequency:
                filters &= Q(price_daily__lte=price_max)
            if filters:
                queryset = RentProperty.objects.filter(filters)
            return queryset
        
        elif purpose.lower() == 'buy':
            self.serializer_class = BuyPropertySerializer
            status = self.request.query_params.get('status', None)
            price_min = self.request.query_params.get('price_min', None)
            price_max = self.request.query_params.get('price_max', None)
            if status:
                filters &= Q(status=status)
            if price_min:
                filters &= Q(price__gte=price_min)
            if price_max:
                filters &= Q(price__lte=price_max)
            if filters:
                queryset = BuyProperty.objects.filter(filters)
            return queryset
        else:
            return queryset