from django.db import models
from decimal import Decimal

TWOPLACES = Decimal(10) ** -2


class Client(models.Model):
    name = models.CharField(max_length=64)
    address = models.TextField()

    def __str__(self):
        return self.name


class Invoice(models.Model):
    name = models.CharField(max_length=256)
    comments = models.TextField(blank=True, null=True)
    client = models.ForeignKey(Client, related_name='invoices')

    def __str__(self):
        return self.name

    @property
    def net_total(self):
        return sum(item.net_total for item in self.items.all())

    @property
    def vat_total(self):
        return sum(item.vat_total for item in self.items.all())

    @property
    def gross_total(self):
        return sum(item.gross_total for item in self.items.all())


class InvoiceItem(models.Model):
    description = models.CharField(max_length=256)
    quantity = models.IntegerField()
    vat = models.DecimalField(max_digits=4, decimal_places=2)
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    invoice = models.ForeignKey(Invoice, related_name='items')

    def __str__(self):
        return self.description

    @property
    def total_rate(self):
        return 1 + self.vat / Decimal('100.00')

    @property
    def gross_amount(self):
        return (self.amount * self.total_rate).quantize(TWOPLACES)

    @property
    def net_total(self):
        return (self.quantity * self.amount).quantize(TWOPLACES)

    @property
    def vat_total(self):
        return (self.quantity * self.amount * self.vat / Decimal('100')).quantize(TWOPLACES)

    @property
    def gross_total(self):
        return (self.quantity * self.gross_amount).quantize(TWOPLACES)
