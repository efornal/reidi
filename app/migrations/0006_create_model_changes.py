# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-04 14:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_create_model_state'),
    ]

    operations = [
        migrations.CreateModel(
            name='Changes',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='creado')),
                ('description', models.TextField(blank=True, null=True, verbose_name='descripci\xf3n')),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Application', verbose_name='application')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.State', verbose_name='state')),
            ],
            options={
                'db_table': 'changes',
                'verbose_name': 'Modificar',
                'verbose_name_plural': 'Changes',
            },
        ),
        migrations.AddField(
            model_name='application',
            name='state',
            field=models.ManyToManyField(through='app.Changes', to='app.State'),
        ),
    ]