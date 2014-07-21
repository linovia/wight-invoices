import pytest

from django.core.urlresolvers import reverse
from django.test.client import Client
from django.contrib.contenttypes.models import ContentType

from wightinvoices.invoice import factories, models
from wightinvoices.history.models import History


@pytest.mark.django_db
def test_action_created_for_estimates():
    client = factories.Client.create()
    owner = factories.User.create(password="clear$abc$toto")
    test_client = Client()
    assert test_client.login(username=owner.username, password="toto")
    data = {
        'client': client.id,
        'name': 'workflow estimate',
        'status': 'draft',
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
    response = test_client.post(reverse('estimate-new'), data=data, follow=True)

    # Check the form is valid
    # response.redirect_chain
    assert response.status_code == 200
    assert hasattr(response, 'redirect_chain')

    # Make sure we have a new estimate creation action
    last_action = History.objects.all().order_by('-id')[0]
    assert last_action.action == 'created'
    assert last_action.content_type == ContentType.objects.get(app_label="invoice", model="estimate")
    assert last_action.object_id == '1'
    assert last_action.user == owner

    estimate = models.Estimate.objects.all().order_by('-id')[0]

    # Now update the estimate
    data['items-à-quantity'] = 2
    response = test_client.post(reverse('estimate-update', kwargs={'estimate_id': estimate.id}), data=data, follow=True)

    # Check the form is valid
    # response.redirect_chain
    assert response.status_code == 200
    assert hasattr(response, 'redirect_chain')

    # Make sure we have a new estimate creation action
    last_action = History.objects.all().order_by('-id')[0]
    assert last_action.action == 'updated'
    assert last_action.content_type == ContentType.objects.get(app_label="invoice", model="estimate")
    assert last_action.object_id == '1'
    assert last_action.user == owner

    # Validate the estimate
    response = test_client.get(reverse('estimate-validate', kwargs={'estimate_id': estimate.id}), follow=True)
    assert response.status_code == 200

    # Ensure we marked the estimate as validated
    last_action = History.objects.all().order_by('-id')[0]
    assert last_action.action == 'sent'
    assert last_action.content_type == ContentType.objects.get(app_label="invoice", model="estimate")
    assert last_action.object_id == '1'
    assert last_action.user == owner

    # Refuse the estimate
    response = test_client.get(reverse('estimate-refuse', kwargs={'estimate_id': estimate.id}), follow=True)
    assert response.status_code == 200

    # Ensure we marked the estimate as validated
    last_action = History.objects.all().order_by('-id')[0]
    assert last_action.action == 'refused'
    assert last_action.content_type == ContentType.objects.get(app_label="invoice", model="estimate")
    assert last_action.object_id == '1'
    assert last_action.user == owner

    # Move the estimate back into sent state
    estimate = models.Estimate.objects.get(id=estimate.id)
    estimate.status = 'sent'
    estimate.save()

    # Accept the estimate
    response = test_client.get(reverse('estimate-accept', kwargs={'estimate_id': estimate.id}), follow=True)
    assert response.status_code == 200

    # Ensure we marked the estimate as validated
    last_action = History.objects.all().order_by('-id')[0]
    assert last_action.action == 'accepted'
    assert last_action.content_type == ContentType.objects.get(app_label="invoice", model="estimate")
    assert last_action.object_id == '1'
    assert last_action.user == owner


@pytest.mark.django_db
def test_action_created_for_invoices():
    client = factories.Client.create()
    owner = factories.User.create(password="clear$abc$toto")
    test_client = Client()
    assert test_client.login(username=owner.username, password="toto")
    data = {
        'client': client.id,
        'name': "Invoice's history",
        'status': 'draft',
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

    # Make sure we have a new invoice creation action
    last_action = History.objects.all().order_by('-id')[0]
    assert last_action.action == 'created'
    assert last_action.content_type == ContentType.objects.get(app_label="invoice", model="invoice")
    assert last_action.object_id == '1'
    assert last_action.user == owner

    invoice = models.Invoice.objects.all().order_by('-id')[0]

    # Now update the invoice
    data['items-à-quantity'] = 2
    response = test_client.post(reverse('invoice-update', kwargs={'invoice_id': invoice.id}), data=data, follow=True)

    # Check the form is valid
    # response.redirect_chain
    assert response.status_code == 200
    assert hasattr(response, 'redirect_chain')

    # Make sure we have a new invoice creation action
    last_action = History.objects.all().order_by('-id')[0]
    assert last_action.action == 'updated'
    assert last_action.content_type == ContentType.objects.get(app_label="invoice", model="invoice")
    assert last_action.object_id == '1'
    assert last_action.user == owner

    # Validate the invoice
    response = test_client.get(reverse('invoice-validate', kwargs={'invoice_id': invoice.id}), follow=True)
    assert response.status_code == 200

    # Ensure we marked the invoice as validated
    last_action = History.objects.all().order_by('-id')[0]
    assert last_action.action == 'unpaid'
    assert last_action.content_type == ContentType.objects.get(app_label="invoice", model="invoice")
    assert last_action.object_id == '1'
    assert last_action.user == owner

    # Refuse the invoice
    response = test_client.get(reverse('invoice-paid', kwargs={'invoice_id': invoice.id}), follow=True)
    assert response.status_code == 200

    # Ensure we marked the invoice as validated
    last_action = History.objects.all().order_by('-id')[0]
    assert last_action.action == 'paid'
    assert last_action.content_type == ContentType.objects.get(app_label="invoice", model="invoice")
    assert last_action.object_id == '1'
    assert last_action.user == owner

    # Move the invoice back into sent state
    invoice = models.Invoice.objects.get(id=invoice.id)
    invoice.status = 'draft'
    invoice.save()

    # Accept the invoice
    response = test_client.get(reverse('invoice-canceled', kwargs={'invoice_id': invoice.id}), follow=True)
    assert response.status_code == 200

    # Ensure we marked the invoice as validated
    last_action = History.objects.all().order_by('-id')[0]
    assert last_action.action == 'canceled'
    assert last_action.content_type == ContentType.objects.get(app_label="invoice", model="invoice")
    assert last_action.object_id == '1'
    assert last_action.user == owner
