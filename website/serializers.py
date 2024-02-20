from rest_framework import serializers
from .models import NavMenu, SocialMedia

class NavMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = NavMenu
        fields = '__all__'

class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = '__all__'
