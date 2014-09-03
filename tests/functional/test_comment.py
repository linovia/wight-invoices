import pytest

from django.core.urlresolvers import reverse
from django.test.client import Client

from wightinvoices.invoice import factories, models
from guardian.shortcuts import assign_perm


@pytest.mark.django_db
def test_estimates_comment_creation():
    owner = factories.User.create(password="clear$abc$toto")
    test_client = Client()
    assert test_client.login(username=owner.username, password="toto")

    estimate = factories.Estimate.create(status='sent', owner=owner)
    assign_perm('view_estimate', owner, estimate)

    assert estimate.comments.count() == 0

    response = test_client.post(reverse('estimate-detail',
            kwargs={'estimate_id': estimate.id}),
        data={'comment': 'Some comment'},
        follow=True)

    assert response.status_code == 200
    assert hasattr(response, 'redirect_chain')

    assert estimate.comments.count() == 1
    comment = estimate.comments.all()[0]
    assert comment.comment == 'Some comment'
    assert comment.user_id == owner.id


@pytest.mark.django_db
def test_estimates_comment_creation_for_unauthorized():
    user = factories.User.create(password="clear$abc$toto")
    test_client = Client()
    assert test_client.login(username=user.username, password="toto")

    estimate = factories.Estimate.create(status='sent')
    assign_perm('view_estimate', estimate.owner, estimate)

    assert estimate.comments.count() == 0

    response = test_client.post(reverse('estimate-detail',
            kwargs={'estimate_id': estimate.id}),
        data={'comment': 'Some comment'},
        follow=True)

    assert response.status_code == 404
    assert estimate.comments.count() == 0


@pytest.mark.django_db
def test_invoices_comment_creation():
    owner = factories.User.create(password="clear$abc$toto")
    test_client = Client()
    assert test_client.login(username=owner.username, password="toto")

    invoice = factories.Invoice.create(status='sent', owner=owner)
    assign_perm('view_invoice', owner, invoice)

    assert invoice.comments.count() == 0

    response = test_client.post(reverse('invoice-detail',
            kwargs={'invoice_id': invoice.id}),
        data={'comment': 'Some comment'},
        follow=True)

    assert response.status_code == 200
    assert hasattr(response, 'redirect_chain')

    assert invoice.comments.count() == 1
    comment = invoice.comments.all()[0]
    assert comment.comment == 'Some comment'
    assert comment.user_id == owner.id


@pytest.mark.django_db
def test_invoices_comment_creation_for_unauthorized():
    user = factories.User.create(password="clear$abc$toto")
    test_client = Client()
    assert test_client.login(username=user.username, password="toto")

    invoice = factories.Invoice.create(status='sent')
    assign_perm('view_invoice', invoice.owner, invoice)

    assert invoice.comments.count() == 0

    response = test_client.post(reverse('invoice-detail',
            kwargs={'invoice_id': invoice.id}),
        data={'comment': 'Some comment'},
        follow=True)

    assert response.status_code == 404
    assert invoice.comments.count() == 0
