from django.urls import path, include
from rest_framework.routers import DefaultRouter

from master_data.rest_view import *

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'products', ProductViewSet)
router.register(r'invoices', InvoiceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
