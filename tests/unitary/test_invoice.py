from decimal import Decimal
import pytest
from wightinvoices.invoice import models


def create_invoice():
    client = models.Client(name='a', address='b')
    client.save()

    invoice = models.Invoice()
    invoice.client = client
    invoice.save()
    # Item #1 / 300 net
    item = models.InvoiceItem()
    item.vat = Decimal('20.0')
    item.amount = Decimal('100.00')
    item.quantity = 3
    item.invoice = invoice
    item.save()
    # Item #2 / 10 net
    item = models.InvoiceItem()
    item.vat = Decimal('20.0')
    item.amount = Decimal('10.00')
    item.quantity = 1
    item.invoice = invoice
    item.save()

    return invoice

@pytest.mark.django_db
def test_net_total():
    invoice = create_invoice()
    assert invoice.net_total == Decimal('310.00')


@pytest.mark.django_db
def test_gross_total():
    invoice = create_invoice()
    assert invoice.gross_total == Decimal('372.00')
