# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-19 11:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_field_document_on_person'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='area',
        ),
        migrations.DeleteModel(
            name='Area',
        ),
    ]
