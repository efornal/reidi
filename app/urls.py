# -*- coding: utf-8 -*-
from django.conf.urls import include
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^login/$', auth_views.login,name='login'),
    url(r'^logout/message',views.logout_message, name='logout_message'),
    url(r'^logout/$', auth_views.logout,{'next_page': 'logout_message'},name='logout'),
    url(r'^en/$', views.index, name='index'),
    url(r'^signup/$', views.sign_up, name='sign_up'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^request_account/$', views.request_account, name='request_account'),
    url(r'^lang/(?P<lang>\w+)/$', views.set_language, name='set_language'),
    url(r'^$', views.index, name='index'),
]
