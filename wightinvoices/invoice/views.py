from django.core.urlresolvers import reverse
from django.views import generic

from . import models


class InvoiceMixin(object):
    model = models.Invoice
    pk_url_kwarg = 'invoice_id'

    def get_success_url(self):
        return reverse('invoice-detail', args=[self.object.id])


class InvoiceList(InvoiceMixin, generic.ListView):
    pass


class InvoiceCreation(InvoiceMixin, generic.CreateView):
    pass


class InvoiceUpdate(InvoiceMixin, generic.UpdateView):
    pass


class InvoiceDetail(InvoiceMixin, generic.DetailView):
    pass
