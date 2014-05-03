from decimal import Decimal
from wightinvoices.invoice import models


def test_gross_amount():
    item = models.InvoiceItem()
    item.vat = Decimal('20.0')
    item.amount = Decimal('100.00')
    assert item.gross_amount == Decimal('120.00')
