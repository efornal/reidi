# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-29 14:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_create_model_documenttype'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='Nombre')),
                ('description', models.TextField(blank=True, null=True, verbose_name='descripci\xf3n')),
            ],
            options={
                'db_table': 'areas',
                'verbose_name': 'Area',
                'verbose_name_plural': 'Areas',
            },
        ),
    ]
