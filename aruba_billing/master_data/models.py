import os

from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=100, verbose_name="nome", blank=False, null=False)
    address = models.TextField(verbose_name="indirizzo", blank=False, null=False)
    fiscal_code = models.CharField(max_length=16, unique=True, verbose_name="codice fiscale", blank=False, null=False)
    vat_number = models.CharField(max_length=16, unique=True, verbose_name="P.IVA", blank=False, null=False)

    class Meta:
        verbose_name = "cliente"
        verbose_name_plural = "clienti"

    def __str__(self):
        return f"{ self.name } - P.IVA: {self.vat_number}"

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="nome", blank=False, null=False)
    description = models.TextField(verbose_name="descrizione", blank=False,null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="prezzo", blank=False,null=False)
    quantity_in_stock = models.PositiveIntegerField(default=0, verbose_name="quantità in magazzino")

    class Meta:
        verbose_name = "prodotto"
        verbose_name_plural = "prodotti"

    def __str__(self):
        return f"{self.name} - Prezzo: {self.price}"

class Invoice(models.Model):
    invoice_number = models.CharField(max_length=20, unique=True, verbose_name="numero fattura", blank=False, null=False)
    issuance_date = models.DateField(verbose_name="data di emissione")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="importo totale", blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=False, null=False)
    products = models.ManyToManyField(Product, through='InvoiceDetail')
    invoice_signed_in_cades = models.BooleanField(default=False, blank=True, verbose_name="Firmato", help_text="spunta se firmato")

    class Meta:
        verbose_name = "fattura"
        verbose_name_plural = "fatture"

    def update_total_amount(self):
        total_amount = sum(detail.product.price * detail.quantity for detail in self.invoice_details.all())
        self.total_amount = total_amount
        self.save()

    def get_total_amount(self):
        try:
            if self.pk:
                total_amount = sum(detail.product.price * detail.quantity for detail in self.invoice_details.all())
            else:
                total_amount = 0
            return total_amount
        except Exception as e:
            total_amount = 0
            print(f"Errore nel calcolo della fattura: {e}")
            return total_amount

    def save(self, *args, **kwargs):

        self.total_amount = self.get_total_amount()
        super().save(*args, **kwargs)
        #TODO: Comunica con il servizio di Fatturazione Elettronica di Aruba per inviare la fattura.

    def __str__(self):
        return self.invoice_number

class InvoiceDetail(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='invoice_details', verbose_name="fattura")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="prodotto")
    quantity = models.PositiveIntegerField(default=0,null=True, verbose_name="quantità")

    class Meta:
        verbose_name = "dettaglio fattura"
        verbose_name_plural = "dettaglio fatture"

    def __str__(self):
        return f"Dettaglio {self.invoice.invoice_number} - {self.product.name}"


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.invoice.update_total_amount()

