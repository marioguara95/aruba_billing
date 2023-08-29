from django.contrib import admin
from .models import Client, Product, Invoice, InvoiceDetail

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'fiscal_code', 'vat_number')
    search_fields = ('name', 'fiscal_code', 'vat_number')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity_in_stock')
    search_fields = ('name',)

class InvoiceDetailInline(admin.TabularInline):
    model = InvoiceDetail
    extra = 1

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'issuance_date', 'total_amount', 'client')
    readonly_fields = ('total_amount',)
    search_fields = ('invoice_number', 'client__name')
    inlines = [InvoiceDetailInline]
