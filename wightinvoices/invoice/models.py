from decimal import Decimal
from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

TWOPLACES = Decimal(10) ** -2


INVOICE_STATUS = (
    ('draft', _('Draft')),
    ('unpaid', _('Unpaid')),
    ('late', _('Late')),
    ('paid', _('Paid')),
    ('canceled', _('Canceled')),
)


ESTIMATE_STATUS = (
    ('draft', _('Draft')),
    ('sent', _('Sent')),
    ('accepted', _('Accepted')),
    ('refused', _('Refused')),
)


class Client(models.Model):
    name = models.CharField(max_length=64)
    address = models.TextField()

    def __str__(self):
        return self.name


class BaseInvoice(models.Model):
    name = models.CharField(max_length=256)
    comments = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="owned_%(class)ss")
    client = models.ForeignKey(Client, related_name='%(class)s')

    class Meta:
        abstract = True

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

    def get_absolute_url(self):
        return reverse('invoice-detail', kwargs={'invoice_id': self.id})


class BaseItem(models.Model):
    description = models.CharField(max_length=256)
    quantity = models.IntegerField()
    vat = models.DecimalField(max_digits=4, decimal_places=2)
    amount = models.DecimalField(max_digits=11, decimal_places=2)

    class Meta:
        abstract = True

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


class Invoice(BaseInvoice):
    status = models.CharField(max_length=64, choices=INVOICE_STATUS, default='draft')

    class Meta:
        permissions = (
            ('view_invoice', 'View invoice'),
        )


class InvoiceItem(BaseItem):
    invoice = models.ForeignKey(Invoice, related_name='items')


class Estimate(BaseInvoice):
    status = models.CharField(max_length=64, choices=ESTIMATE_STATUS, default='draft')

    class Meta:
        permissions = (
            ('view_estimate', 'View estimate'),
        )

    def is_draft(self):
        return self.status == 'draft'

    def is_published(self):
        return self.status == 'sent'


class EstimateItem(BaseItem):
    estimate = models.ForeignKey(Estimate, related_name='items')
