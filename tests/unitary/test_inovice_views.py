import pytest

from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse
from django.test.client import RequestFactory
from  django.core.exceptions import PermissionDenied

from guardian.shortcuts import assign_perm

from wightinvoices.invoice import views, factories, models


@pytest.mark.django_db
def test_invoice_creation_view():
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
    invoice_count = models.Invoice.objects.count()
    request_factory = RequestFactory()
    user = factories.User.create()
    request = request_factory.post(reverse('invoice-new'), data=data)
    request.user = user
    response = views.InvoiceCreation.as_view()(request)
    # Check the form is valid and we have an extra invoice.
    assert response.status_code == 302
    assert invoice_count + 1 == models.Invoice.objects.count()
    # Get the latest invoice and check the item's count and description
    invoice = models.Invoice.objects.order_by('-id').all()[0]
    assert invoice.items.count() == 1
    assert invoice.items.all()[0]. description == 'Computer'
    # Now make sure the creator has access permission
    assert user.has_perm('view_invoice', invoice) == True
    assert invoice.owner == user


@pytest.mark.django_db
def test_invoice_update_view():
    invoice = factories.Invoice.create()
    data = {
        'client': invoice.client.id,
        'name': 'demo invoice',
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
    request_factory = RequestFactory()
    request = request_factory.post(reverse('invoice-update', args=[invoice.id]), data=data)
    request.user = invoice.owner
    response = views.InvoiceUpdate.as_view()(request, invoice_id=invoice.id)
    # Check the form is valid and we have an extra invoice.
    assert response.status_code == 302
    # Get the latest invoice and check the item's count and description
    original_invoice = invoice
    invoice = models.Invoice.objects.get(id=original_invoice.id)

    assert invoice.name == data['name']

    assert invoice.items.count() == 1
    assert invoice.items.all()[0]. description == 'Computer'


@pytest.mark.django_db
def test_invoice_can_not_be_updated_by_random_user():
    invoice = factories.Invoice.create()
    request_factory = RequestFactory()
    user = factories.User.create()
    view = views.InvoiceUpdate.as_view()
    request = request_factory.get(reverse('invoice-update', args=[invoice.id]))
    request.user = user
    with pytest.raises(PermissionDenied):
        view(request, invoice_id=invoice.id)
    request = request_factory.post(reverse('invoice-update', args=[invoice.id]), data={})
    request.user = user
    with pytest.raises(PermissionDenied):
        view(request, invoice_id=invoice.id)


@pytest.mark.django_db
def test_invoice_permission_update():
    view = views.InvoiceUpdate.as_view()
    invoice = factories.Invoice.create()
    user1 = factories.User.create()
    user2 = factories.User.create()
    owner = invoice.owner
    data = {
        'client': invoice.client.id,
        'name': 'demo invoice',
        'cc': [user1.id],
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
    request_factory = RequestFactory()

    request = request_factory.post(reverse('invoice-update', args=[invoice.id]), data=data)
    request.user = invoice.owner
    response = view(request, invoice_id=invoice.id)
    assert response.status_code == 302
    assert owner.has_perm('view_invoice', invoice)
    assert user1.has_perm('view_invoice', invoice)
    assert not user2.has_perm('view_invoice', invoice)

    data['cc'] = [user2.id]
    request = request_factory.post(reverse('invoice-update', args=[invoice.id]), data=data)
    request.user = invoice.owner
    response = view(request, invoice_id=invoice.id)
    assert response.status_code == 302
    assert owner.has_perm('view_invoice', invoice)
    assert not user1.has_perm('view_invoice', invoice)
    assert user2.has_perm('view_invoice', invoice)


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

