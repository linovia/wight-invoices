from decimal import Decimal
from wightinvoices.invoice import models


def test_gross_amount():
    item = models.InvoiceItem()
    item.vat = Decimal('20.0')
    item.amount = Decimal('100.00')
    assert item.gross_amount == Decimal('120.00')


def test_net_total():
    item = models.InvoiceItem()
    item.vat = Decimal('20.0')
    item.amount = Decimal('100.00')
    item.quantity = 3
    assert item.net_total == Decimal('300.00')


def test_gross_total():
    item = models.InvoiceItem()
    item.vat = Decimal('20.0')
    item.amount = Decimal('100.00')
    item.quantity = 3
    assert item.gross_total == Decimal('360.00')


def test_vat_total():
    item = models.InvoiceItem()
    item.vat = Decimal('20.0')
    item.amount = Decimal('100.00')
    item.quantity = 3
    assert item.vat_total == Decimal('60.00')
