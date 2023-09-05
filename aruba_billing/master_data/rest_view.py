from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Client, Product, Invoice, InvoiceDetail
from .serializers import ClientSerializer, ProductSerializer, InvoiceSerializer

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer


    # Altri metodi della view
    def create(self, request, *args, **kwargs):
        client = request.data.get("client")
        # Creazione o recupero del cliente
        name = client.pop('name')
        address = client.pop('address')
        fiscal_code = client.pop('fiscal_code')
        vat_number = client.pop('vat_number')

        try:
            existing_client = Client.objects.get(fiscal_code=fiscal_code)
            client_instance = existing_client
        except:
            client_instance = Client.objects.create(name=name,
                                     address=address,
                                     fiscal_code=fiscal_code,
                                     vat_number=vat_number
                                     )

        invoice_number = request.data.get("invoice_number")
        issuance_date = request.data.get("issuance_date")

        try:
            invoice_instance = Invoice.objects.get(invoice_number=invoice_number)
        except:
            invoice_instance = Invoice.objects.create(invoice_number=invoice_number,
                              issuance_date=issuance_date,
                              total_amount=0, #L'importo totale viene calcolato durante il salvataggio dei prodotti
                              client=client_instance)

        products_data = request.data.get('products')

        for product in products_data:
            product_name = product.pop('name')
            product_description = product.pop('description')
            product_price = product.pop('price')
            product_quantity_in_stock = product.pop('quantity_in_stock')
            product_quantity = product.pop('quantity')

            try:
                product = Product.objects.get(name=product_name, description=product_description)
            except Product.DoesNotExist:
                product = Product.objects.create(name=product_name,
                                                 description=product_description,
                                                 price=product_price,
                                                 quantity_in_stock=product_quantity_in_stock
                                                 )

            InvoiceDetail.objects.create(invoice=invoice_instance, product=product, quantity=product_quantity)

        return Response({'message': 'Fattura creata con successo', 'invoice_id': invoice_instance.id})


    @action(methods=["get"], detail=False)
    def invoices_in_interval(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        invoice_id = request.query_params.get('invoice_id')

        if not start_date and not end_date and not invoice_id:
            return Response({'error': 'At least one of start_date, end_date, or invoice_id must be provided.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if start_date:
            try:
                start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
            except ValueError:
                return Response({'error': 'Invalid start_date format. Use YYYY-MM-DD format.'},
                                status=status.HTTP_400_BAD_REQUEST)

        if end_date:
            try:
                end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()
            except ValueError:
                return Response({'error': 'Invalid end_date format. Use YYYY-MM-DD format.'},
                                status=status.HTTP_400_BAD_REQUEST)

        invoices = Invoice.objects.all()

        if start_date and end_date:
            invoices = invoices.filter(issuance_date__range=(start_date, end_date))
        elif start_date:
            invoices = invoices.filter(issuance_date__gte=start_date)
        elif end_date:
            invoices = invoices.filter(issuance_date__lte=end_date)

        if invoice_id:
            invoices = invoices.filter(invoice_number=invoice_id)

        serializer = self.get_serializer(invoices, many=True)

        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def invoice_status(self, request, pk=None):
        invoice = self.get_object()
        total_amount = invoice.get_total_amount()  # Chiamata al metodo che calcola l'importo
        return Response({'status': 'Paid', 'total_amount': total_amount})

