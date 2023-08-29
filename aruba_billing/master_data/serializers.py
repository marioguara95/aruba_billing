from rest_framework import serializers, status
from rest_framework.response import Response

from .models import Client, Product, Invoice, InvoiceDetail


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class InvoiceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceDetail
        fields = '__all__'


class InvoiceSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    client = ClientSerializer()

    class Meta:
        model = Invoice
        fields = '__all__'

