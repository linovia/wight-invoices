from django.http import HttpResponseRedirect
from django.forms.models import modelformset_factory
from django.core.urlresolvers import reverse
from django.views import generic

from guardian.mixins import PermissionRequiredMixin

from . import models, forms


class InvoiceMixin(object):
    """
    A mixin that describes Invoice model.
    """
    model = models.Invoice
    pk_url_kwarg = 'invoice_id'
    form_class = forms.Invoice

    def get_success_url(self):
        return reverse('invoice-detail', args=[self.object.id])


class ItemInvoiceProcessMixin(object):
    """
    A mixin that renders a form & formset on GET and processes it on POST.
    """

    def get_formset_kwargs(self):
        args = self.get_form_kwargs()
        args.pop('instance', None)
        args['prefix'] = 'items'
        args['queryset'] = models.InvoiceItem.objects.none()
        if self.object:
            args['queryset'] = self.object.items.all()
        return args

    def get_formset(self):
        InvoiceItemFormSet = modelformset_factory(models.InvoiceItem, form=forms.InvoiceItem, can_delete=True)
        return InvoiceItemFormSet(**self.get_formset_kwargs())

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates a blank version of the form and
        the formset.
        """
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = self.get_formset()

        return self.render_to_response(self.get_context_data(
            form=form, formset=formset,
            formset_helper=forms.InvoiceItemHelper()))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = self.get_formset()
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        """
        If the formset is valid, save the associated models.
        """
        self.object = form.save()
        items = formset.save(commit=False)
        for item in items:
            item.invoice = self.object
            item.save()
        for item in formset.deleted_objects:
            item.delete()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, formset):
        """
        If the forms are invalid, re-render the context data with the
        data-filled form, formset and errors.
        """
        return self.render_to_response(self.get_context_data(
            form=form, formset=formset,
            formset_helper=forms.InvoiceItemHelper()))


class CreateMixin(object):
    """
    Base mixin for creating an new object instance.
    """
    def get(self, request, *args, **kwargs):
        self.object = None
        return super(CreateMixin, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        return super(CreateMixin, self).post(request, *args, **kwargs)


class UpdateMixin(object):
    """
    Base mixin for updating an existing object.
    """
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(UpdateMixin, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(UpdateMixin, self).post(request, *args, **kwargs)


class InvoiceList(InvoiceMixin, generic.ListView):
    pass


class InvoiceCreation(InvoiceMixin, CreateMixin, ItemInvoiceProcessMixin, generic.CreateView):
    pass

class InvoiceUpdate(InvoiceMixin, UpdateMixin, ItemInvoiceProcessMixin, generic.UpdateView):
    pass


class InvoiceDetail(PermissionRequiredMixin,
        InvoiceMixin, generic.DetailView):
    permission_required = 'view_invoice'
    return_403 = True
