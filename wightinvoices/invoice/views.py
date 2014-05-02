from django.shortcuts import render
from django.views import generic

from . import models


class InvoiceList(generic.ListView):
    model = models.Invoice


class InvoiceDetail(generic.DetailView):
    model = models.Invoice
    pk_url_kwarg = 'invoice_id'
