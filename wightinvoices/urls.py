from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',
    url(r'^', include('wightinvoices.invoice.urls')),
    url(r'^client/', include('wightinvoices.clients.urls')),
    url(r'^api/', include('wightinvoices.api.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
)
