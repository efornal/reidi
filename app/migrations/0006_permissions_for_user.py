# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-16 11:19
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0005_create_model_application'),
    ]

    operations = [
        migrations.RunSQL(
            "GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO reidi_user;",
            "REVOKE SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public FROM reidi_user;"
         ),
        migrations.RunSQL(
            "GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO reidi_user;",
            "REVOKE ALL ON ALL SEQUENCES IN SCHEMA public FROM reidi_user;"
        ),
    ]
