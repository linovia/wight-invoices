from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import generic
from django.core.urlresolvers import reverse

from . import models, forms


class ClientMixin(object):
    """
    A mixin that describes Client model.
    """
    model = models.Client
    pk_url_kwarg = 'invoice_id'
    form_class = forms.Client

    def get_success_url(self):
        return reverse('client-detail', args=[self.object.id])

    def get_queryset(self):
        return super(ClientMixin, self).get_queryset

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ClientMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs = super(ClientMixin, self).get_context_data(**kwargs)
        kwargs['activemenu'] = 'client'
        return kwargs
