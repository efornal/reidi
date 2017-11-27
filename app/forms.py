# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import logging
import dns.resolver, dns.exception
from django.utils.translation import ugettext as _
from django.conf import settings

    
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

        
