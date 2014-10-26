
from operator import attrgetter
import itertools

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import generic
from django.core.urlresolvers import reverse

from wightinvoices.invoice.models import Invoice, Estimate
from . import models, forms


class ClientMixin(object):
    """
    A mixin that describes Client model.
    """
    model = models.Client
    pk_url_kwarg = 'client_id'
    form_class = forms.Client

    def get_success_url(self):
        return reverse('client-detail', args=[self.object.id])

    def get_queryset(self):
        return super(ClientMixin, self).get_queryset()

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ClientMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs = super(ClientMixin, self).get_context_data(**kwargs)
        kwargs['activemenu'] = 'client'
        return kwargs


class ClientList(ClientMixin, generic.ListView):
    pass


class ClientCreation(ClientMixin, generic.CreateView):
    pass


class ClientUpdate(ClientMixin, generic.UpdateView):
    pass


class ClientDetail(ClientMixin, generic.DetailView):
    def get_context_data(self, **kwargs):
        kwargs = super(ClientMixin, self).get_context_data(**kwargs)
        def add_type(type_value):
            def _add_type(item):
                item.type = type_value
                return item
            return _add_type
        invoices = map(add_type('Invoice'), Invoice.objects.filter(client=self.object))
        estimates = map(add_type('Estimate'), Estimate.objects.filter(client=self.object))
        items = sorted(itertools.chain(invoices, estimates), key=attrgetter('creation_date'))
        kwargs['items'] = items
        return kwargs
