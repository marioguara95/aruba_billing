from django.urls import path, include
from rest_framework.routers import DefaultRouter

from master_data.csv import generate_csv_report
from master_data.rest_view import *
from master_data.views import custom_view

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'products', ProductViewSet)
router.register(r'invoices', InvoiceViewSet)
urlpatterns = [
    path('', custom_view, name="custom_view"),
    path('api/', include(router.urls)),
    path('generate_csv_report/', generate_csv_report, name='generate_csv_report'),

]

