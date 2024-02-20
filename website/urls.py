from django.urls import path
from .views import NavMenuListAPIView, SocialMediaListAPIView

urlpatterns = [
    path('api/navmenus/', NavMenuListAPIView.as_view(), name='navmenu-list'),
    path('api/socialmedias/', SocialMediaListAPIView.as_view(), name='socialmedia-list'),
]
