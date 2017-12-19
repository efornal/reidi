# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import logging
from .models import Application
from .models import Domain
from .models import Person
from .models import DocumentType
from .models import State
from datetimewidget.widgets import DateTimeWidget
import dns.resolver, dns.exception
from django.utils.translation import ugettext as _
from django.conf import settings
from datetime import datetime
from validators import validate_email_domain_restriction
from validators import validate_existence_email_domain


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required',
                             validators=[validate_email_domain_restriction,
                                         validate_existence_email_domain])


    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(_('email_must_be_unique'))
        return email

    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')



class ResetPasswordForm(forms.ModelForm):
    email = forms.EmailField(
        max_length=200,
        help_text='Required',
        validators=[validate_email_domain_restriction,
                    validate_existence_email_domain])
    class Meta:
        model = User
        fields = ('email',)

        

class DefinePasswordForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('password1', 'password2')


        
class EditUserForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=150, 
        required=True,
        label=_('first_name'))
    last_name = forms.CharField(
        max_length=150, 
        required=True,
        label=_('last_name'))
    email = forms.EmailField(
        max_length=255,
        help_text='Required',
        validators=[validate_email_domain_restriction,
                    validate_existence_email_domain])

    class Meta:
        model = User
        fields = ('first_name','last_name','email',)
        
class EditPersonForm(forms.ModelForm):
    document_type = forms.ModelChoiceField(
        queryset=DocumentType.objects.all(),
        to_field_name = "id",
        required = True,
        empty_label=_('empty_label_select_field'),
        label=_('document_type'))
    document_number = forms.CharField(
        max_length=20, 
        required=True,
        label=_('document_number'))
    telephone_number = forms.CharField(
        max_length=255, 
        required=False,
        label=_('telephone_number'))

    class Meta:
        model = Person
        fields = ('telephone_number','document_type', 'document_number')


class ApplicationForm(forms.ModelForm):
    resource = forms.CharField(
        max_length=255, 
        required=True,
        label=_('resource'))
    area = forms.CharField(
        max_length=255, 
        required=True,
        label=_('area'))
    date_from = forms.DateTimeField(
        required=True,
        label=_('date_from'))
    date_until = forms.DateTimeField(
        required=True,
        label=_('date_until'))
    objectives = forms.CharField(
        required=False,
        label=_('objectives'),
        widget=forms.Textarea)
    requirements = forms.CharField(
        required=False,
        label=_('requirements'),
        widget=forms.Textarea)
    domain = forms.ModelChoiceField(
        queryset=Domain.objects.all(),
        empty_label=_('empty_label_select_field'),
        to_field_name = "id",
        required = True,
        label=_('domain'))
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        to_field_name = "id",
        required = True,
        label=_('user'))
    

    def clean(self):
        cleaned_data = super(ApplicationForm, self).clean()
        date_from = cleaned_data.get('date_from')
        date_until = cleaned_data.get('date_until')
        if date_from > date_until:
            self.add_error('date_from', _('date_from_previous_date_until'))
            
    class Meta:
        model = Application
        fields = ('domain', 'objectives', 'requirements',
                  'resource','area','user','date_from', 'date_until')

        
class ChangeForm(forms.ModelForm):
    application = forms.ModelChoiceField(
        queryset=Application.objects.all(),
        to_field_name = "id",
        required = True,
        label=_('application'))
    state = forms.ModelChoiceField(
        queryset=State.objects.all(),
        to_field_name = "id",
        required = True,
        label=_('state'))
