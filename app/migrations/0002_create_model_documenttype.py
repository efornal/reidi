# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-29 14:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_create_model_domain'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'document_types',
                'verbose_name': 'Tipo de documento',
                'verbose_name_plural': 'Tipos de documentos',
            },
        ),
    ]
