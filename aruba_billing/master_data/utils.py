from django.http import FileResponse, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.views import View

from master_data.models import Invoice

#TODO implementabile inserendo un campo file
"""
class DownloadInvoiceView(View):
    def get(self, request, pk):
        # Trova il invoice con l'ID specificato
        invoice = get_object_or_404(Invoice, pk=pk)
        if invoice.file:
            # Verifica se la fattura è firmata in CADES
            if invoice.invoice_signed_in_cades:
                # Se è firmata in CADES, restituisci un file con la fattura non firmata
                non_firmata_file = invoice.file_non_firmata
                if non_firmata_file:
                    response = FileResponse(non_firmata_file)
                    response['Content-Type'] = non_firmata_file.url.split('.')[-1]
                    response['Content-Disposition'] = f'attachment; filename="{non_firmata_file.name}"'
                    return response
                else:
                    return HttpResponseNotFound("File non firmato non disponibile")
            else:
                # Se la fattura non è firmata in CADES, restituisci il file della fattura
                response = FileResponse(invoice.file)
                response['Content-Type'] = invoice.file.url.split('.')[-1]
                response['Content-Disposition'] = f'attachment; filename="{invoice.file.name}"'
                return response

        return HttpResponseNotFound("File non trovato")"""
