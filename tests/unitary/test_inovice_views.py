import pytest
from django.core.urlresolvers import reverse
from django.test.client import RequestFactory
from wightinvoices.invoice import views, factories, models


@pytest.mark.django_db
def test_invoice_creation_view():
    client = factories.Client.create()
    invoice_count = models.Invoice.objects.count()
    factory = RequestFactory()
    data = {
        'client': client.id,
        'name': 'demo invoice',
        'items-TOTAL_FORMS': u'1',
        'items-INITIAL_FORMS': u'0',
        'items-MIN_NUM_FORMS': u'0',
        'items-MAX_NUM_FORMS': u'1000',
        'items-0-description': 'Computer',
        'items-0-quantity': 1,
        'items-0-vat': 20.0,
        'items-0-amount': 1000,
    }
    request = factory.post(reverse('invoice-new'), data=data)
    response = views.InvoiceCreation.as_view()(request)
    assert response.status_code == 302
    assert invoice_count + 1 == models.Invoice.objects.count()
    invoice = models.Invoice.objects.order_by('-id').all()[0]
    assert invoice.items.count() == 1
