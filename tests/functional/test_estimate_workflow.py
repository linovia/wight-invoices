import pytest
from lxml import etree

from django.core.urlresolvers import reverse
from django.test.client import Client

from wightinvoices.invoice import factories, models



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

    html = etree.HTML(data)
    update = html.xpath("//a[text()='Update estimate']")
    validate = html.xpath("//a[text()='Validate']")
    accept = html.xpath("//a[text()='Accept']")
    refuse = html.xpath("//a[text()='Refuse']")

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

    html = etree.HTML(data)
    update = html.xpath("//a[text()='Update estimate']")
    validate = html.xpath("//a[text()='Validate']")
    accept = html.xpath("//a[text()='Accept']")
    refuse = html.xpath("//a[text()='Refuse']")

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
