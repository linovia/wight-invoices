from wightinvoices.invoice import models
from rest_framework import serializers



class NestedInvoiceItem(serializers.ModelSerializer):
    class Meta:
        model = models.InvoiceItem
        fields = ('id', 'description', 'quantity', 'vat', 'amount')


class Invoice(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(slug_field='email')
    client = serializers.SlugRelatedField(slug_field='name')
    items = NestedInvoiceItem(many=True, read_only=True)

    class Meta:
        model = models.Invoice
        fields = ('id', 'notes', 'owner', 'client', 'status', 'items')
