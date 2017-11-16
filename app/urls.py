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
    url(r'^account/signup/$', views.account_sign_up, name='account_sign_up'),
    url(r'^account/activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.account_activate, name='account_activate'),
    url(r'^account/create/$', views.account_create, name='account_create'),
    url(r'^lang/(?P<lang>\w+)/$', views.set_language, name='set_language'),
    url(r'^$', views.index, name='index'),
]
