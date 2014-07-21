import pytest

from django.core.urlresolvers import reverse
from django.test.client import Client
from django.contrib.contenttypes.models import ContentType

from wightinvoices.invoice import factories, models
from wightinvoices.history.models import History


@pytest.mark.django_db
def test_action_created_for_new_estimate():
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
    assert last_action.action == 'new'
    assert last_action.content_type == ContentType.objects.get(app_label="invoice", model="estimate")
    assert last_action.object_id == '1'

