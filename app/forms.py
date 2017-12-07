# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import logging
from .models import Application
from .models import Domain
from .models import Person
from .models import DocumentType
from .models import Area
from datetimewidget.widgets import DateTimeWidget
import dns.resolver, dns.exception
from django.utils.translation import ugettext as _
from django.conf import settings
from datetime import datetime
    
def validate_email_domain_restriction(value):
    logging.info('Checking email domain in preset domains..')
    valid_domains = []
    try:
        email_domain = value.split('@')[1]
        valid_domains = settings.VALIDATE_EMAIL_DOMAINS
    except AttributeError, e:
        logging.warning("Email domain verification is omitted. %s", e)
    except Exception, e:
        logging.warning("Email domain verification failed. %s", e)
        raise forms.ValidationError(_('email_domain_not_exist'))
    
    if email_domain not in valid_domains:
        logging.warning("Invalid email domain {}, valid are {}"
                        .format(email_domain, valid_domains))
        raise forms.ValidationError(_('email_domain_restriction'))
    return value


def validate_existence_email_domain(value):
    logging.info('Checking the existence of the email domain..')
    validate = False
    try:
        validate = settings.VALIDATE_EXISTENCE_EMAIL_DOMAIN
    except AttributeError, e:
        logging.warning("Email domain existence is omitted. %s", e)
        return value
    
    try:
        if validate:
            email_domain = value.split('@')[1]
            results = dns.resolver.query(email_domain, 'MX')
    except dns.exception.DNSException, e:
        logging.warning('Domain does not exist. %s', e)
        raise forms.ValidationError(_('email_domain_not_exist'))
    except Exception, e:
        logging.error('ERROR Exception: %s',e)

    return value




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
        empty_label=_('empty_label_document_type'),
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
    objectives = forms.CharField(widget=forms.Textarea)
    date_from = forms.DateTimeField(
        required=True,
        label=_('date_from'))
    date_until = forms.DateTimeField(
        required=True,
        label=_('date_until'))
    requirements = forms.CharField(widget=forms.Textarea)
    domain = forms.ModelChoiceField(
        queryset=Domain.objects.all(),
        to_field_name = "id",
        required = True,
        label=_('domain'))
    area = forms.ModelChoiceField(
        queryset=Area.objects.all(),
        to_field_name = "id",
        required = True,
        label=_('area'))
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        to_field_name = "id",
        required = True,
        label=_('user'))
    

    class Meta:
        model = Application
        fields = ('domain', 'area', 'objectives', 'requirements',
                  'resource','user','date_from', 'date_until')

