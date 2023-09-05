from decimal import Decimal
from django.test import TestCase
from .models import Invoice, Client, Product, InvoiceDetail

class InvoiceModelTest(TestCase):
    def setUp(self):
        # Crea un cliente di esempio
        self.client = Client.objects.create(name="Cliente Test")

        # Crea un prodotto di esempio con un quantity_in_stock valido
        self.product = Product.objects.create(name="Prodotto Test", price=10.00, quantity_in_stock=50)

    def test_save_with_valid_data(self):
        # Crea una fattura valida
        invoice = Invoice.objects.create(
            invoice_number="567",
            issuance_date="2023-09-05",
            client=self.client
        )

        # Crea un dettaglio di fattura collegato al prodotto di esempio
        invoice_detail = InvoiceDetail.objects.create(
            invoice=invoice,
            product=self.product,
            quantity=2
        )

        # Chiama la funzione save del modello Invoice
        invoice.save()

        # Verifica che il totale sia stato calcolato correttamente
        self.assertEqual(invoice.total_amount, 20.00)
        print("Test 'test_save_with_valid_data' superato con successo.")

    def test_save_with_invalid_data(self):
        # Prova a creare una fattura con dati non validi
        with self.assertRaises(Exception):
            invalid_invoice = Invoice()
            invalid_invoice.save()
        print("Test 'test_save_with_invalid_data' superato con successo.")

    def test_save_with_invoice_details(self):
        # Crea una fattura valida
        invoice = Invoice.objects.create(
            invoice_number="125",
            issuance_date="2023-09-07",
            client=self.client
        )

        # Crea un dettaglio di fattura collegato al prodotto di esempio
        invoice_detail = InvoiceDetail(
            invoice=invoice,
            product=self.product,
            quantity=3
        )

        # Chiama la funzione save del modello InvoiceDetail prima di salvare la fattura
        invoice_detail.save()

        # Chiama la funzione save del modello Invoice
        invoice.save()

        # Verifica che il totale sia stato calcolato correttamente
        self.assertEqual(invoice.total_amount, 30.00)
        print("Test 'test_save_with_invoice_details' superato con successo.")

class InvoiceDetailModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="Prodotto Test", price=10.00)
        self.client = Client.objects.create(name="Cliente Test")
        self.invoice = Invoice.objects.create(invoice_number="12345", issuance_date="2023-09-05", client=self.client)
        self.invoice_detail = InvoiceDetail.objects.create(invoice=self.invoice, product=self.product, quantity=2)

    def test_invoice_detail_save_updates_total_amount(self):
        new_invoice_detail = InvoiceDetail.objects.create(invoice=self.invoice, product=self.product, quantity=3)
        self.invoice.refresh_from_db()
        updated_total_amount = self.invoice.total_amount
        expected_total_amount = self.product.price * (self.invoice_detail.quantity + new_invoice_detail.quantity)
        self.assertEqual(updated_total_amount, expected_total_amount)
        print("Test 'test_invoice_detail_save_updates_total_amount' superato con successo.")
