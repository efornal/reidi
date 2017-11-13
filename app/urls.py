# -*- coding: utf-8 -*-
from django.conf.urls import include
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^login/$', auth_views.login,name='login'),
    url(r'^logout/$', auth_views.logout,{'next_page': 'logout_message'},name='logout'),
    url(r'^en/$', views.index, name='index'),
    url(r'^lang/(?P<lang>\w+)/$', views.set_language, name='set_language'),
    url(r'^$', views.index, name='index'),
]
