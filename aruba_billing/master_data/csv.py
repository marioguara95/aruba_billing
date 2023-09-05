import csv
from datetime import datetime, timedelta
from django.http import HttpResponse
from .models import Invoice


def generate_csv_report(request):
    day_param = request.GET.get('day')

    if day_param:
        selected_day = datetime.strptime(day_param, '%Y-%m-%d')
    else:
        selected_day = datetime.now()

    invoices_selected_day = Invoice.objects.filter(issuance_date=selected_day)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="invoice_report_{selected_day.strftime("%Y-%m-%d")}.csv"'

    csv_writer = csv.writer(response, delimiter=';')
    csv_writer.writerow(['File Name', 'SDI Identifier', 'Invoice Date', 'Total', 'Client'])

    for invoice in invoices_selected_day:
        csv_writer.writerow([
            invoice.file.name if invoice.file else '',
            invoice.invoice_number if invoice.invoice_number else '',
            invoice.issuance_date.strftime('%Y-%m-%d') if invoice.issuance_date else '',
            invoice.total_amount if invoice.total_amount else '',
            invoice.client if invoice.client else ''
        ])

    return response
