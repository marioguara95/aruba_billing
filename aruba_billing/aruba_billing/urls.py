from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from oauth2_provider.views import AuthorizationView, TokenView

urlpatterns = [
    path('', include('master_data.urls')),
    path('admin/', admin.site.urls),
    path('oauth/authorize/', AuthorizationView.as_view(), name="authorize"),
    path('oauth/token/', TokenView.as_view(), name="token"),
    path('oauth/callback/', RedirectView.as_view(), name="callback"),

]
