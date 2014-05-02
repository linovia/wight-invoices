from django.conf.urls import patterns, url
from django.contrib import admin
from . import views

urlpatterns = patterns('',
    url(r'^invoice/$', views.InvoiceList.as_view(), name='invoice-list'),
)
