from django.urls import path
from .views import NavMenuListAPIView, SocialMediaListAPIView

urlpatterns = [
    path('navmenus/', NavMenuListAPIView.as_view(), name='navmenu-list'),
    path('socialmedias/', SocialMediaListAPIView.as_view(), name='socialmedia-list'),
]
