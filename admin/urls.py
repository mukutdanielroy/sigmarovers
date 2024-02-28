"""
URL configuration for admin project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views 

admin.site.site_header = 'Sigma Rovers Real Estate L.L.C'                    # default: "Django Administration"
# admin.site.index_title = 'Features area'                 # default: "Site administration"
# admin.site.site_title = 'HTML title from adminsitration'

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('media/government_id_photos/<str:filename>', views.serve_government_id_photo, name='serve_government_id_photo'),
    path('api/', include('website.urls')),
    path('api/', include('property.urls')),
    path('api/', include('user.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)