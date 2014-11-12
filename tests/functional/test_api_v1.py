import pytest
from decimal import Decimal
from django.core.urlresolvers import reverse
from rest_framework.test import APIClient
from wightinvoices.invoice import factories, models


pytestmark = pytest.mark.django_db
api_client = APIClient()


def test_invoice_detail():
    owner = factories.User.create(password="clear$abc$toto")
    assert api_client.login(username=owner.username, password="toto")

    client = factories.Client.create()
    invoice = factories.Invoice.create(client=client)
    invoice_item = factories.InvoiceItem.create(invoice=invoice)

    url = reverse('api-invoice-detail', kwargs={'pk': invoice.id})
    response = api_client.get(url, format='json')

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


def test_invoice_create():
    """
    Regular invoice creation
    """
    owner = factories.User.create(password="clear$abc$toto")
    assert api_client.login(username=owner.username, password="toto")

    client = factories.Client.create(name='myclient')

    invoice_data = {
        'client': 'myclient',
        'notes': 'N/A',
        'status': 'draft',
        'items': [{
            'description': 'qwerty',
            'quantity': 5,
            'vat': '20.00',
            'amount': '100.00',
        }]
    }

    url = reverse('api-invoice-list')
    response = api_client.post(url, data=invoice_data, format='json')

    assert response.status_code == 201, response.data

    invoice = models.Invoice.objects.order_by('-id').first()
    assert invoice.notes == 'N/A'
    assert invoice.client.name == 'myclient'
    assert invoice.owner_id == owner.id
    assert invoice.status == 'draft'
    assert invoice.items.count() == 1
    item = invoice.items.all()[0]
    assert item.quantity == 5


def test_invoice_create_for_another_owner():
    """
    We need to make sure we can't create an invoice on behalf of someone else
    """
    owner = factories.User.create(password="clear$abc$toto")
    assert api_client.login(username=owner.username, password="toto")

    non_owner = factories.User.create()
    client = factories.Client.create(name='myclient')

    invoice_data = {
        'client': 'myclient',
        'notes': 'N/A',
        'status': 'draft',
        'owner': 'non_owner',
        'items': [{
            'description': 'qwerty',
            'quantity': 5,
            'vat': '20.00',
            'amount': '100.00',
        }]
    }

    url = reverse('api-invoice-list')
    response = api_client.post(url, data=invoice_data, format='json')

    assert response.status_code == 201, response.data

    invoice = models.Invoice.objects.order_by('-id').first()
    assert invoice.notes == 'N/A'
    assert invoice.client.name == 'myclient'
    assert invoice.owner_id == owner.id
    assert invoice.status == 'draft'
    assert invoice.items.count() == 1
    item = invoice.items.all()[0]
    assert item.quantity == 5
