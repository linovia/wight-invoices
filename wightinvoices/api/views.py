
from rest_framework import viewsets

from wightinvoices.invoice import models
from . import serializers


class Invoice(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing invoices.
    """
    queryset = models.Invoice.objects.all()
    serializer_class = serializers.Invoice

    def get_queryset(self):
        return models.Invoice.objects.all().select_related('owner', 'client').prefetch_related('items')
