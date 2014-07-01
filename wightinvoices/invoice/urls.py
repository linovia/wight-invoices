from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^invoice/$', views.InvoiceList.as_view(), name='invoice-list'),
    url(r'^invoice/new/$', views.InvoiceCreation.as_view(), name='invoice-new'),
    url(r'^invoice/(?P<invoice_id>\d+)/$', views.InvoiceDetail.as_view(), name='invoice-detail'),
    url(r'^invoice/(?P<invoice_id>\d+)/update/$', views.InvoiceUpdate.as_view(), name='invoice-update'),

    url(r'^estimate/$', views.EstimateList.as_view(), name='estimate-list'),
    url(r'^estimate/new/$', views.EstimateCreation.as_view(), name='estimate-new'),
    url(r'^estimate/(?P<estimate_id>\d+)/$', views.EstimateDetail.as_view(), name='estimate-detail'),
    url(r'^estimate/(?P<estimate_id>\d+)/update/$', views.EstimateUpdate.as_view(), name='estimate-update'),
    url(r'^estimate/(?P<estimate_id>\d+)/accept/$', views.EstimateAccept.as_view(), name='estimate-accept'),
    url(r'^estimate/(?P<estimate_id>\d+)/refuse/$', views.EstimateRefuse.as_view(), name='estimate-refuse'),
    url(r'^estimate/(?P<estimate_id>\d+)/validate/$', views.EstimateValidate.as_view(), name='estimate-validate'),
)
