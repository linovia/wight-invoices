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
