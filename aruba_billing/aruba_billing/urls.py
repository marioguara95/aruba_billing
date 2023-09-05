from django.contrib import admin
from django.contrib.auth import login
from django.template.defaulttags import url
from django.urls import path, include

urlpatterns = [
    path('', include('master_data.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('auth/', include('social_django.urls', namespace='social')),
]
