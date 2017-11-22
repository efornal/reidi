# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import logging
import dns.resolver, dns.exception
from django.utils.translation import ugettext as _


def validate_email_domain_restriction(value):
    logging.info('Checking email domain in preset domains..')
    email_domain = value.split('@')[1]
    valid_domains = ['unl.edu.ar','rectorado.unl.edu.ar']
    if email_domain not in valid_domains:
        logging.warning("Invalid email domain {}, valid are {}"
                        .format(email_domain, valid_domains))
        raise forms.ValidationError(_('email_domain_restriction'))
    return value


def validate_existence_email_domain(value):
    logging.info('Checking the existence of the email domain..')
    try:
        email_domain = value.split('@')[1]
        results = dns.resolver.query(email_domain, 'MX')
    except dns.exception.DNSException, e:
        logging.warning('Domain %s does not exist.', e)
        raise forms.ValidationError(_('email_domain_not_exist'))
    return value


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required',
                             validators=[validate_email_domain_restriction,
                                         validate_existence_email_domain])


    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
