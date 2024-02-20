from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PropertyTypeCategoryViewSet, BuyPropertyListAPIView, BuyPropertyDetailAPIView, RentPropertyListAPIView, RentPropertyDetailAPIView, BookingListAPIView, BookingDetailAPIView, PropertySearchAPIView

router = DefaultRouter()
router.register(r'property-type-categories', PropertyTypeCategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('buy-properties/', BuyPropertyListAPIView.as_view(), name='buy-property-list'),
    path('buy-properties/<int:pk>/', BuyPropertyDetailAPIView.as_view(), name='buy-property-detail'),
    path('rent-properties/', RentPropertyListAPIView.as_view(), name='rent-property-list'),
    path('rent-properties/<int:pk>/', RentPropertyDetailAPIView.as_view(), name='rent-property-detail'),
    path('bookings/', BookingListAPIView.as_view(), name='booking-list'),
    path('bookings/<int:pk>/', BookingDetailAPIView.as_view(), name='booking-detail'),
    path('search/', PropertySearchAPIView.as_view(), name='property-search-by-location'),
]
