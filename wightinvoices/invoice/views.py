from django.core.urlresolvers import reverse
from django.views import generic

from . import models


class InvoiceList(generic.ListView):
    model = models.Invoice


class InvoiceCreation(generic.CreateView):
    model = models.Invoice

    def get_success_url(self):
        return reverse('invoice-detail', args=[self.object.id])


class InvoiceUpdate(generic.UpdateView):
    model = models.Invoice
    pk_url_kwarg = 'invoice_id'

    def get_success_url(self):
        return reverse('invoice-detail', args=[self.object.id])


class InvoiceDetail(generic.DetailView):
    model = models.Invoice
    pk_url_kwarg = 'invoice_id'
