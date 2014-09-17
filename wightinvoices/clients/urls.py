from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.ClientList.as_view(), name='client-list'),
    url(r'^new/$', views.ClientCreation.as_view(), name='client-new'),
    url(r'^(?P<client_id>\d+)/$', views.ClientDetail.as_view(), name='client-detail'),
    url(r'^(?P<client_id>\d+)/update/$', views.ClientUpdate.as_view(), name='client-update'),
)
