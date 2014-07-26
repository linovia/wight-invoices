import pytest

from django.core.urlresolvers import reverse
from django.test.client import Client
from django.contrib.contenttypes.models import ContentType

from wightinvoices.invoice import factories, models
from wightinvoices.history.models import History


@pytest.mark.django_db
def test_action_created_for_invoices():
    client = factories.Client.create()
    owner = factories.User.create(password="clear$abc$toto")
    user = factories.User.create(password="clear$abc$toto")
    test_client = Client()
    assert test_client.login(username=owner.username, password="toto")
    test_client2 = Client()
    assert test_client2.login(username=user.username, password="toto")
    data = {
        'client': client.id,
        'name': "Invoice's history",
        'cc': [user.id],
        'items-TOTAL_FORMS': u'1',
        'items-INITIAL_FORMS': u'0',
        'items-MIN_NUM_FORMS': u'0',
        'items-MAX_NUM_FORMS': u'1000',
        'items-0-id': "",
        'items-0-description': 'Computer',
        'items-0-quantity': 1,
        'items-0-vat': 20.0,
        'items-0-amount': 1000,
    }
    response = test_client.post(reverse('invoice-new'), data=data, follow=True)

    # Check the form is valid
    # response.redirect_chain
    assert response.status_code == 200
    assert hasattr(response, 'redirect_chain')

    invoice = models.Invoice.objects.all().order_by('-id')[0]

    # Validate the invoice
    response = test_client.get(reverse('invoice-validate', kwargs={'invoice_id': invoice.id}), follow=True)
    assert response.status_code == 200

    # Pay the invoice
    response = test_client2.get(reverse('invoice-paid', kwargs={'invoice_id': invoice.id}), follow=True)
    assert response.status_code == 403
    response = test_client.get(reverse('invoice-paid', kwargs={'invoice_id': invoice.id}), follow=True)
    assert response.status_code == 200

    # Move the invoice back into sent state
    invoice = models.Invoice.objects.get(id=invoice.id)
    invoice.status = 'draft'
    invoice.save()

    # Cancel the invoice
    response = test_client2.get(reverse('invoice-cancel', kwargs={'invoice_id': invoice.id}), follow=True)
    assert response.status_code == 403
    response = test_client.get(reverse('invoice-cancel', kwargs={'invoice_id': invoice.id}), follow=True)
    assert response.status_code == 200
