# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from app.models import Application
from app.models import Area
from app.models import Domain


# Register your models here.

admin.site.register(Area)
admin.site.register(Domain)
admin.site.register(Application)
