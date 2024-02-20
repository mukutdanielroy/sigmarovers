from rest_framework import generics
from .models import PropertyTypeCategory, BuyProperty, RentProperty, Booking, Property
from .serializers import PropertyTypeCategorySerializer, BuyPropertySerializer, RentPropertySerializer, BookingSerializer, PropertySerializer
from rest_framework import viewsets

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

class BookingListAPIView(generics.ListAPIView):
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
        location_name = self.request.query_params.get('location', None)
        status = self.request.query_params.get('status', None)
        if purpose == 'Rent':
            if location_name:
                self.serializer_class = BuyPropertySerializer  # Change serializer class
                # Filter BuyProperty queryset by location name
                return RentProperty.objects.filter(location__name__icontains=location_name)
        elif purpose == 'Buy':
            self.serializer_class = BuyPropertySerializer  # Change serializer class
            # Filter BuyProperty queryset by location name
            return BuyProperty.objects.filter(location__name__icontains=location_name, status=status)
        else:
            # If location parameter is not provided, return an empty queryset
            return Property.objects.none()