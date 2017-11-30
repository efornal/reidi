# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from app.models import Application
from app.models import Area
from app.models import Domain
from app.models import DocumentType

class ApplicationAdmin(admin.ModelAdmin):
    search_fields = ['resoruce','domain','user']
    ordering = ('resource',)
    list_display = ('resource','domain','user')
    list_filter = ('domain','area','user')

admin.site.register(Area)
admin.site.register(Domain)
admin.site.register(DocumentType)
admin.site.register(Application, ApplicationAdmin)
