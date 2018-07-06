# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from app.models import Application
from app.models import Domain
from app.models import State
from app.models import Change
from app.models import Person
from app.models import DocumentType
from django import forms


    
class ChangesInline(admin.TabularInline):
   model = Application.states.through
   extra = 1


class ApplicationAdmin(admin.ModelAdmin):
    search_fields = ['resoruce','domain','user','area']
    ordering = ('resource',)
    list_display = ('domain','resource','user')
    list_filter = ('domain','user')

    inlines = [ChangesInline,]

    
class StateAdmin(admin.ModelAdmin):
    search_fields = ['name']
    ordering = ('name',)
    list_display = ('name','is_default')
    
class ChangeAdmin(admin.ModelAdmin):
    search_fields = ['state__name']
    ordering = ('state__name',)
    list_display = ('application', 'state','created_at')
    list_filter = ('application','state')
    
    
admin.site.register(Domain)
admin.site.register(DocumentType)
admin.site.register(State,StateAdmin)
admin.site.register(Change, ChangeAdmin)
admin.site.register(Person)
admin.site.register(Application, ApplicationAdmin)
