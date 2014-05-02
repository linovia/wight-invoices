from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^invoice/$', views.InvoiceList.as_view(), name='invoice-list'),
    url(r'^invoice/(?P<invoice_id>\d+)/$', views.InvoiceDetail.as_view(), name='invoice-detail'),
)
