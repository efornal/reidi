# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _


class State(models.Model):
    id = models.AutoField(
        primary_key=True,
        null=False)
    name = models.CharField(
        max_length=255,
        null=False,
        verbose_name=_('name'))
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('description'))
    is_default = models.BooleanField(
        default=False,
        verbose_name=_('is_default'))
    icon_link = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('icon_link'))

    class Meta:
        db_table = 'states'
        verbose_name = _('State')
        verbose_name_plural = _('States')

    def __unicode__(self):
        return self.name
    

class Domain(models.Model):
    id = models.AutoField(
        primary_key=True,
        null=False)
    name = models.CharField(
        max_length=255,
        null=False,
        verbose_name=_('name'))

    class Meta:
        db_table = 'domains'
        verbose_name = _('Domain')
        verbose_name_plural = _('Domains')

    def __unicode__(self):
        return self.name

    
class DocumentType(models.Model):
    id = models.AutoField(
        primary_key=True,
        null=False)
    name = models.CharField(
        max_length=255,
        null=False)
    
    class Meta:
        db_table = 'document_types'
        verbose_name = _('DocumentType')
        verbose_name_plural = _('DocumentTypes')
        
    def __unicode__(self):
        return self.name

    
# class Area(models.Model):
#     id = models.AutoField(
#         primary_key=True,
#         null=False)
#     name = models.CharField(
#         max_length=255,
#         null=False,
#         verbose_name=_('name'))
#     description = models.TextField(
#         null=True,
#         blank=True,
#         verbose_name=_('description'))

#     class Meta:
#         db_table = 'areas'
#         verbose_name = _('Area')
#         verbose_name_plural = _('Areas')

#     def __unicode__(self):
#         return self.name

    
class Application(models.Model):
    id = models.AutoField(
        primary_key=True,
        null=False)
    user = models.ForeignKey(
        User,
        null=False,
        default=None,
        verbose_name=_('user'))
    resource = models.CharField(
        max_length=255,
        null=False,
        verbose_name=_('resource'))
    objectives = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('objectives'))
    requirements = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('requirements'))
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created_at'))
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('updated_at'))
    date_from = models.DateTimeField(
        verbose_name=_('date_from'))
    date_until = models.DateTimeField(
        verbose_name=_('date_until'))
    area = models.CharField(
        max_length=255,
        null=False,
        verbose_name=_('area'))
    domain = models.ForeignKey(
        Domain,
        null=False,
        verbose_name=_('domain'))
    states = models.ManyToManyField(
        State,
        through='Change')

    class Meta:
        db_table = 'applications'
        verbose_name = _('Application')
        verbose_name_plural = _('Applications')

    def __unicode__(self):
        return self.resource

    def last_state(self):
        return self.states.last()
        
    
class Change(models.Model):
    id = models.AutoField(
        primary_key=True,
        null=False)
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        verbose_name=_('application'))
    state = models.ForeignKey(
        State,
        on_delete=models.CASCADE,
        verbose_name=_('state'))
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created_at'))
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('description'))

    class Meta:
        db_table = 'changes'
        verbose_name = _('Change')
        verbose_name_plural = _('Changes')

    def __unicode__(self):
        return self.state.name

    
class Person(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('user'))
    telephone_number = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('telephone_number'))
    document_type = models.ForeignKey(
        DocumentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_('document_type'))
    document_number = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name=_('document_number'))
    class Meta:
        db_table = 'people'
        verbose_name = _('Person')
        verbose_name_plural = _('People')

    def __unicode__(self):
        return self.user.username
