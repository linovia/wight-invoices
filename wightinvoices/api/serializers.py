from wightinvoices.invoice import models
from wightinvoices.clients.models import Client
from rest_framework import serializers


class NestedInvoiceItem(serializers.ModelSerializer):
    class Meta:
        model = models.InvoiceItem
        fields = ('id', 'description', 'quantity', 'vat', 'amount')


class ListNestedInvoiceItem(serializers.ListSerializer):
    child = NestedInvoiceItem()

    def to_representation(self, data):
        """
        List of object instances -> List of dicts of primitive datatypes.
        """
        return serializers.ReturnList(
            [self.child.to_representation(item) for item in data.all()],
            serializer=self
        )


class Invoice(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(slug_field='email', read_only=True)
    client = serializers.SlugRelatedField(slug_field='name', queryset=Client.objects.all())
    # items = ListNestedInvoiceItem()
    items = NestedInvoiceItem(many=True)

    class Meta:
        model = models.Invoice
        fields = ('id', 'notes', 'owner', 'client', 'status', 'items')

        extra_kwargs = {
            'owner': {'read_only': True}
        }

    def create(self, validated_data):
        print(validated_data)
        items_data = validated_data.pop('items', [])
        validated_data['owner'] = self.context['request'].user
        invoice = models.Invoice.objects.create(**validated_data)
        for item_data in items_data:
            print('Creating: %s' % item_data)
            models.InvoiceItem.objects.create(invoice=invoice, **item_data)
        return invoice