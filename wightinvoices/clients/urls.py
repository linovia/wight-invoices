from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^client/$', views.ClientList.as_view(), name='client-list'),
    url(r'^client/new/$', views.ClientCreation.as_view(), name='client-new'),
    url(r'^client/(?P<client_id>\d+)/$', views.ClientDetail.as_view(), name='client-detail'),
    url(r'^client/(?P<client_id>\d+)/update/$', views.ClientUpdate.as_view(), name='client-update'),
)
