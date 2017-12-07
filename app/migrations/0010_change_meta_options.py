# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-06 11:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_add_field_icon_link_to_state'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='change',
            options={'verbose_name': 'Cambio', 'verbose_name_plural': 'Cambios'},
        ),
        migrations.AlterModelOptions(
            name='state',
            options={'verbose_name': 'Estado', 'verbose_name_plural': 'Estados'},
        ),
        migrations.AlterField(
            model_name='area',
            name='name',
            field=models.CharField(max_length=255, verbose_name='nombre'),
        ),
        migrations.AlterField(
            model_name='change',
            name='application',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Application', verbose_name='solicitud'),
        ),
        migrations.AlterField(
            model_name='change',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.State', verbose_name='estado'),
        ),
        migrations.AlterField(
            model_name='domain',
            name='name',
            field=models.CharField(max_length=255, verbose_name='nombre'),
        ),
        migrations.AlterField(
            model_name='state',
            name='icon_link',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='link de icono'),
        ),
        migrations.AlterField(
            model_name='state',
            name='is_default',
            field=models.BooleanField(default=False, verbose_name='usar por defecto'),
        ),
        migrations.AlterField(
            model_name='state',
            name='name',
            field=models.CharField(max_length=255, verbose_name='nombre'),
        ),
    ]