# -*- coding: utf-8 -*-
from django.conf.urls import include
from django.conf.urls import url
from . import views
from . import registration
from . import auth
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^accounts/edit/$', auth.edit, name='auth_edit'),
    url(r'^accounts/save/$', auth.save, name='auth_save'),
    url(r'^accounts/login/$', auth_views.login,name='login'),
    url(r'^logout/message', auth.logout_message, name='logout_message'),
    url(r'^logout/$', auth_views.logout,{'next_page': 'logout_message'},name='logout'),
    url(r'^en/$', views.index, name='index'),
    url(r'^application/new/$', views.application_new, name='application_new'),
    url(r'^application/list/$', views.application_list, name='application_list'),
    url(r'^application/create/$', views.application_create, name='application_create'),

    url(r'^accounts/password/reset/$', auth.password_reset, name='auth_password_reset'),
    url(r'^accounts/password/reset/complete/$', auth.password_reset_complete, name='auth_password_reset_complete'),
    url(r'^accounts/password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth.password_reset_confirm, name='auth_password_reset_confirm'),
    url(r'^accounts/password/change/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth.password_change, name='auth_password_change'),

    url(r'^accounts/register/$', registration.register, name='registration_register'),
    url(r'^accounts/register/complete/$', registration.complete, name='registration_complete'),
    url(r'^accounts/activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', registration.activate, name='registration_activate'),
    url(r'^lang/(?P<lang>\w+)/$', views.set_language, name='set_language'),
    url(r'^$', views.index, name='index'),
]
