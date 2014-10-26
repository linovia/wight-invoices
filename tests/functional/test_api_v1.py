import pytest
from decimal import Decimal
from django.core.urlresolvers import reverse
from rest_framework.test import APIClient
from wightinvoices.invoice import factories


pytestmark = pytest.mark.django_db
api_client = APIClient()


def test_invoice_detail():
    owner = factories.User.create(password="clear$abc$toto")
    assert api_client.login(username=owner.username, password="toto")

    invoice = factories.Invoice.create()
    invoice_item = factories.InvoiceItem.create(invoice=invoice)

    url = reverse('api-invoice-detail', kwargs={'pk': invoice.id})
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data == {
        'id': invoice.id,
        'client': 'client1',
        'notes': None,
        'items': [{
            'id': invoice_item.id,
            'description': invoice_item.description,
            'quantity': invoice_item.quantity,
            'vat': '%.02f' % Decimal(invoice_item.vat),
            'amount': '%.02f' % Decimal(invoice_item.amount),
        }],
        'owner': owner.email,
        'status': 'draft',
    }
