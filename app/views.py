# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils import translation
import logging
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm
from .forms import ResetPasswordForm
from .forms import DefinePasswordForm
from .forms import ApplicationForm
from .models import Domain
from .models import Application
from .models import Area
from .models import State
from .models import Change
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.core.exceptions import MultipleObjectsReturned
from django.core.mail import EmailMessage
from django.db import transaction
from django.utils.translation import ugettext as _
from django.contrib import messages

def set_language(request, lang='es'):
    if 'lang' in request.GET:
        lang = request.GET['lang']
    translation.activate(lang)
    request.session[translation.LANGUAGE_SESSION_KEY] = lang
    logging.info("Language changed by the user to '{}'".format(lang))
    return redirect('index')


@login_required
def application_new(request):
    form = ApplicationForm()
    context = {'form': form}
    return render(request, 'application/new.html', context)


@login_required
def application_list(request):
    applications = Application.objects.filter(user=request.user.pk)
    context = {'applications': applications}
    return render(request, 'application/index.html', context)


@login_required
def application_show(request, pk):
    application = Application.objects.get(pk=pk)
    form = ApplicationForm(instance=application)
    context = {'application': application, 'form': form}
    return render(request, 'application/show.html', context)


@login_required
def index(request):
    context={}
    return render(request, 'index.html', context)

def sanitize_application_create_params(request):
    params = request.POST.copy()
    try:
        params['user'] = request.user.pk
        if 'date_from' in params:
            params['date_from'] = unicode( datetime.strptime(params['date_from'],'%d-%m-%Y %H:%M'))
        if 'date_until' in params:
            params['date_until'] = unicode(datetime.strptime(params['date_until'], '%d-%m-%Y %H:%M'))
    except Exception, e:
        logging.error('ERROR Exception',e)
    return params


@login_required
@transaction.atomic
def application_create(request):
    params = sanitize_application_create_params(request)
    form = ApplicationForm(params)
    state = State.objects.filter(is_default=True).first()
    context = {'form': form}
    if form.is_valid():
        sid = transaction.savepoint()
        try:
            logging.warning("creating new application..")
            application = form.save()
            change = Change(application=application, state=state)
            change.save()
            transaction.savepoint_commit( sid )
            context.update({'message': _('create_application_message')})
            return render(request, 'application/create.html', context)
        except Exception as e:
            logging.error('ERROR Exception: %s', e)
            transaction.savepoint_rollback( sid )
            messages.warning(request, _('application_creation_failure_message'))
            #context.update({'message': _('application_creation_failure_message')})
    
    else:
        logging.warning("ERROR creating new application..")
        logging.error(form.errors)
        
    return render(request, 'application/new.html', context)        


    
