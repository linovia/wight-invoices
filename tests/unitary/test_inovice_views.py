import pytest
from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse
from django.test.client import RequestFactory
from guardian.shortcuts import assign_perm
from wightinvoices.invoice import views, factories, models


def create_data():
    client = factories.Client.create()
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
    return data


@pytest.mark.django_db
def test_invoice_creation_view():
    data = create_data()
    invoice_count = models.Invoice.objects.count()
    request_factory = RequestFactory()
    request = request_factory.post(reverse('invoice-new'), data=data)
    response = views.InvoiceCreation.as_view()(request)
    assert response.status_code == 302
    assert invoice_count + 1 == models.Invoice.objects.count()
    invoice = models.Invoice.objects.order_by('-id').all()[0]
    assert invoice.items.count() == 1


def create_request(user, give_perm=False):
    invoice = factories.Invoice.create()
    if give_perm:
        assign_perm('view_invoice', user, invoice)
    request_factory = RequestFactory()
    request = request_factory.get(reverse('invoice-detail', args=[invoice.id]))
    request.user = user
    request.invoice = invoice

    return request


@pytest.mark.django_db
def test_invoice_can_be_viewed_by_authorized_user():
    authorized_user = factories.User.create()
    request = create_request(authorized_user, give_perm=True)
    response = views.InvoiceDetail.as_view()(request, invoice_id=request.invoice.id)
    assert response.status_code == 200


@pytest.mark.django_db
def test_invoice_can_not_be_viewed_by_unauthorized_user():
    unauthorized_user = factories.User.create()
    request = create_request(unauthorized_user, give_perm=False)
    response = views.InvoiceDetail.as_view()(request, invoice_id=request.invoice.id)
    assert response.status_code == 403


@pytest.mark.django_db
def test_invoice_can_not_be_viewed_by_anonymous_user():
    request = create_request(AnonymousUser(), give_perm=False)
    response = views.InvoiceDetail.as_view()(request, invoice_id=request.invoice.id)
    assert response.status_code == 403

