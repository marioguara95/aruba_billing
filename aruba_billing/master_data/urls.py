from django.urls import path, include
from rest_framework.routers import DefaultRouter

from master_data.rest_view import *
from master_data.views import custom_view

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'products', ProductViewSet)
router.register(r'invoices', InvoiceViewSet)
urlpatterns = [
    path('', custom_view, name="custom_view"),
    path('api/', include(router.urls)),

]

