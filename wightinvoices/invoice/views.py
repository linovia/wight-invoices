from django.http import HttpResponseRedirect
from django.forms.models import modelformset_factory
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import generic

from guardian.shortcuts import (assign_perm, remove_perm,
        get_users_with_perms, get_objects_for_user)

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

    def get_queryset(self):
        return get_objects_for_user(self.request.user, 'invoice.view_invoice')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(InvoiceMixin, self).dispatch(*args, **kwargs)


class ItemInvoiceProcessMixin(object):
    """
    A mixin that renders a form & formset on GET and processes it on POST.
    """
    item_model = models.InvoiceItem
    item_form = forms.InvoiceItem
    item_fk = 'invoice'
    view_permission = 'view_invoice'

    def get_initial(self):
        initial = self.initial.copy()
        # Don't query the permissions if the object isn't created yet
        if not self.object:
            return initial
        permissions = get_users_with_perms(self.object, attach_perms=True)
        initial['cc'] = [k for k, v in permissions.items() if self.view_permission in v]
        return initial

    def get_formset_kwargs(self):
        kwargs = {
            'prefix': 'items',
            'queryset': self.item_model.objects.none()
        }
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        if self.object:
            kwargs['queryset'] = self.object.items.all()
        return kwargs

    def get_formset(self):
        ItemFormSet = modelformset_factory(self.item_model, form=self.item_form, can_delete=True)
        return ItemFormSet(**self.get_formset_kwargs())

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

    def update_permissions(self, new_users):
        """
        Assign the invoice's view permissions to the `new_users` list.
        """
        # Retrieve the currently authorized users for view_invoice
        permissions = get_users_with_perms(self.object, attach_perms=True)
        former_authorized_users = set(k for k, v in permissions.items() if self.view_permission in v)

        # Create a new set of authorized users including the owner
        authorized_users = set(new_users)
        authorized_users.add(self.request.user)

        # Authorized added users:
        for user in (authorized_users - former_authorized_users):
            assign_perm(self.view_permission, user, self.object)

        # Revoke removed users:
        for user in (former_authorized_users - authorized_users):
            remove_perm(self.view_permission, user, self.object)

    def form_valid(self, form, formset):
        """
        If the formset is valid, save the associated models.
        """
        # Set the owner as the current user and save the object
        self.object = form.save(commit=False)
        if not self.object.id:
            self.object.owner = self.request.user
        self.object.save()

        # Update object's permissions
        self.update_permissions(form.cleaned_data['cc'])

        # Create / Delete the invoice's items
        items = formset.save(commit=False)
        for item in items:
            setattr(item, self.item_fk, self.object)
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
        if self.object.owner != request.user:
            raise PermissionDenied()
        return super(UpdateMixin, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.owner != request.user:
            raise PermissionDenied()
        return super(UpdateMixin, self).post(request, *args, **kwargs)


class InvoiceList(InvoiceMixin, generic.ListView):
    pass


class InvoiceCreation(InvoiceMixin, CreateMixin, ItemInvoiceProcessMixin, generic.CreateView):
    pass


class InvoiceUpdate(InvoiceMixin, UpdateMixin, ItemInvoiceProcessMixin, generic.UpdateView):
    pass


class InvoiceDetail(InvoiceMixin, generic.DetailView):
    pass


#
# Estimates
#

class EstimateMixin(object):
    """
    A mixin that describes Estimate model.
    """
    model = models.Estimate
    pk_url_kwarg = 'estimate_id'
    form_class = forms.Estimate

    def get_success_url(self):
        return reverse('estimate-detail', args=[self.object.id])

    def get_queryset(self):
        return get_objects_for_user(self.request.user, 'invoice.view_estimate')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EstimateMixin, self).dispatch(*args, **kwargs)


class ItemEstimateProcessMixin(ItemInvoiceProcessMixin):
    item_model = models.EstimateItem
    item_form = forms.EstimateItem
    item_fk = 'estimate'
    view_permission = 'view_estimate'


class EstimateList(EstimateMixin, generic.ListView):
    pass


class EstimateCreation(EstimateMixin, CreateMixin, ItemEstimateProcessMixin, generic.CreateView):
    pass


class EstimateUpdate(EstimateMixin, UpdateMixin, ItemEstimateProcessMixin, generic.UpdateView):
    pass


class EstimateDetail(EstimateMixin, generic.DetailView):
    pass

