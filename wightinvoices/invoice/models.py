from django.db import models


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
