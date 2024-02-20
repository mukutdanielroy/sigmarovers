from django.shortcuts import render

# Create your views here.

from rest_framework import generics
from .models import NavMenu, SocialMedia
from .serializers import NavMenuSerializer, SocialMediaSerializer

class NavMenuListAPIView(generics.ListAPIView):
    queryset = NavMenu.objects.filter(active=True)
    serializer_class = NavMenuSerializer

class SocialMediaListAPIView(generics.ListAPIView):
    queryset = SocialMedia.objects.filter(active=True)
    serializer_class = SocialMediaSerializer
