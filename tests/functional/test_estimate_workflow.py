import pytest
import functools
from lxml import etree
from django.core.urlresolvers import reverse
from django.test.client import Client

from wightinvoices.invoice import factories, models


def get_button(tree, label):
    return tree.xpath("//a[text()='%s']" % label)


@pytest.mark.django_db
def test_estimate_update_view():
    client = factories.Client.create()
    owner = factories.User.create(password="clear$abc$toto")
    test_client = Client()
    assert test_client.login(username=owner.username, password="toto")
    data = {
        'client': client.id,
        'name': 'workflow estimate',
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
    estimate_count = models.Estimate.objects.count()
    response = test_client.post(reverse('estimate-new'), data=data, follow=True)

    find_update_button = functools.partial(get_button, label="Update estimate")
    find_validate_button = functools.partial(get_button, label="Validate")
    find_accept_button = functools.partial(get_button, label="Accept")
    find_refuse_button = functools.partial(get_button, label="Refuse")

    # Check the form is valid
    # response.redirect_chain
    assert response.status_code == 200
    assert hasattr(response, 'redirect_chain')

    # Make sure we have a new invoice and get its ID
    assert models.Estimate.objects.count() == estimate_count + 1

    estimate = models.Estimate.objects.all().order_by('-id')[0]
    assert estimate.name == 'workflow estimate'
    assert estimate.status == 'draft'

    # View the invoice details
    response = test_client.get(reverse('estimate-detail',
        kwargs={'estimate_id': estimate.id}))

    assert response.status_code == 200

    # Ensure we have a button to edit it and one to validate it but
    # none to accept / refuse
    data = response.content.decode('utf8')

    html_tree = etree.HTML(data)
    update = find_update_button(html_tree)
    validate = find_validate_button(html_tree)
    accept = find_accept_button(html_tree)
    refuse = find_refuse_button(html_tree)

    assert update
    assert validate
    assert not accept
    assert not refuse

    # Validate the estimate
    validate = validate[0]
    url = validate.attrib['href']
    response = test_client.get(url, follow=True)

    assert response.status_code == 200

    # Refresh the estimate object
    estimate = models.Estimate.objects.get(id=estimate.id)
    assert estimate.status == 'sent'

    # Ensure we have buttons to accept / refuse the estimate but not
    # buttons for modification / validate
    data = response.content.decode('utf8')

    html_tree = etree.HTML(data)
    update = find_update_button(html_tree)
    validate = find_validate_button(html_tree)
    accept = find_accept_button(html_tree)
    refuse = find_refuse_button(html_tree)

    assert update
    assert not validate
    assert accept
    assert refuse

    accept_url = accept[0].attrib['href']
    refuse_url = refuse[0].attrib['href']

    # Accept the estimate
    response = test_client.get(accept_url, follow=True)
    assert response.status_code == 200
    estimate = models.Estimate.objects.get(id=estimate.id)
    assert estimate.status == 'accepted'

    # Make sure we can not refuse an estimate we already accepted
    response = test_client.get(refuse_url, follow=True)
    assert response.status_code == 200
    estimate = models.Estimate.objects.get(id=estimate.id)
    assert estimate.status == 'accepted'

    # Rolls back the estimate into sent
    estimate.status = 'sent'
    estimate.save()

    # Make sure we can refuse an estimate
    response = test_client.get(refuse_url, follow=True)
    assert response.status_code == 200
    estimate = models.Estimate.objects.get(id=estimate.id)
    assert estimate.status == 'refused'

    # Make sure we can not accept an estimate we already refused
    response = test_client.get(refuse_url, follow=True)
    assert response.status_code == 200
    estimate = models.Estimate.objects.get(id=estimate.id)
    assert estimate.status == 'refused'


@pytest.mark.django_db
def test_invoice_update_view():
    client = factories.Client.create()
    owner = factories.User.create(password="clear$abc$toto")
    test_client = Client()
    assert test_client.login(username=owner.username, password="toto")
    data = {
        'client': client.id,
        'name': 'workflow invoice',
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
    invoice_count = models.Invoice.objects.count()
    response = test_client.post(reverse('invoice-new'), data=data, follow=True)

    find_update_button = functools.partial(get_button, label="Update invoice")
    find_validate_button = functools.partial(get_button, label="Validate")
    find_paid_button = functools.partial(get_button, label="Paid")
    find_cancel_button = functools.partial(get_button, label="Cancel")

    # Check the form is valid
    # response.redirect_chain
    assert response.status_code == 200
    assert hasattr(response, 'redirect_chain')

    # Make sure we have a new invoice and get its ID
    assert models.Invoice.objects.count() == invoice_count + 1

    invoice = models.Invoice.objects.all().order_by('-id')[0]
    assert invoice.name == 'workflow invoice'
    assert invoice.status == 'draft'

    # View the invoice details
    response = test_client.get(reverse('invoice-detail',
        kwargs={'invoice_id': invoice.id}))

    assert response.status_code == 200

    # Ensure we have a button to edit it and one to validate it but
    # none to accept / refuse
    data = response.content.decode('utf8')

    html_tree = etree.HTML(data)
    update = find_update_button(html_tree)
    validate = find_validate_button(html_tree)
    paid = find_paid_button(html_tree)
    cancel = find_cancel_button(html_tree)

    assert update, "Update button not found after creation"
    assert validate, "Validation button not found after creation"
    assert not paid, "Paid button found after creation"
    assert cancel, "Cancel button not found after creation"

    # Validate the invoice
    validate = validate[0]
    url = validate.attrib['href']
    response = test_client.get(url, follow=True)

    assert response.status_code == 200

    # Refresh the invoice object
    invoice = models.Invoice.objects.get(id=invoice.id)
    assert invoice.status == 'unpaid'

    # Ensure we have buttons to accept / refuse the invoice but not
    # buttons for modification / validate
    data = response.content.decode('utf8')

    html_tree = etree.HTML(data)
    update = find_update_button(html_tree)
    validate = find_validate_button(html_tree)
    paid = find_paid_button(html_tree)
    cancel = find_cancel_button(html_tree)

    assert update
    assert not validate
    assert paid
    assert cancel

    accept_url = paid[0].attrib['href']
    refuse_url = cancel[0].attrib['href']

    # Accept the invoice
    response = test_client.get(accept_url, follow=True)
    assert response.status_code == 200
    invoice = models.Invoice.objects.get(id=invoice.id)
    assert invoice.status == 'paid'

    # Make sure we can not refuse an invoice we already accepted
    response = test_client.get(refuse_url, follow=True)
    assert response.status_code == 200
    invoice = models.Invoice.objects.get(id=invoice.id)
    assert invoice.status == 'paid'

    # Rolls back the invoice into sent
    invoice.status = 'unpaid'
    invoice.save()

    # Make sure we can cancel an invoice
    response = test_client.get(refuse_url, follow=True)
    assert response.status_code == 200
    invoice = models.Invoice.objects.get(id=invoice.id)
    assert invoice.status == 'canceled'

    # Make sure we can not accept an invoice we already refused
    response = test_client.get(refuse_url, follow=True)
    assert response.status_code == 200
    invoice = models.Invoice.objects.get(id=invoice.id)
    assert invoice.status == 'canceled'
