from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('master_data.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('auth/', include('social_django.urls', namespace='social')),
]
