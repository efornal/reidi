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
from datetime import timedelta
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm
from .forms import ResetPasswordForm
from .forms import DefinePasswordForm
from .forms import ApplicationForm
from .models import Domain
from .models import Application
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
from django.contrib.auth.decorators import permission_required

def default_date_from():
    return datetime.now().strftime('%d-%m-%Y %H:%M')

def default_date_until():
    increase_days = 365
    if hasattr(settings, 'INCREASE_DAYS_FOR_DATE_UNTIL') and \
       settings.INCREASE_DAYS_FOR_DATE_UNTIL > 0:
        increase_days = settings.INCREASE_DAYS_FOR_DATE_UNTIL
    return (datetime.now()+ timedelta(days=increase_days)).strftime('%d-%m-%Y %H:%M') 


def set_language(request, lang='es'):
    if 'lang' in request.GET:
        lang = request.GET['lang']
    translation.activate(lang)
    request.session[translation.LANGUAGE_SESSION_KEY] = lang
    logging.info("Language changed by the user to '{}'".format(lang))
    return redirect('index')


@login_required
@permission_required('app.add_application')
def application_new(request):
    form = ApplicationForm()
    context = {'form': form,
               'date_from': default_date_from(),
               'date_until': default_date_until()}
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
            params.update(
                {'date_from':
                 unicode( datetime.strptime(params['date_from'],'%d-%m-%Y %H:%M'))})
        if 'date_until' in params:
            params.update(
                {'date_until':
                 unicode(datetime.strptime(params['date_until'], '%d-%m-%Y %H:%M'))})
    except Exception, e:
        logging.error('ERROR Exception',e)
    return params


@login_required
@permission_required('app.add_application')
@transaction.atomic
def application_create(request):
    params = sanitize_application_create_params(request)
    form = ApplicationForm(params)
    state = State.objects.filter(is_default=True).first()
    context = { 'date_from': default_date_from(),
                'date_until': default_date_until()}

    if form.is_valid():
        context = {'form': form}
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
    
    else:
        context.update({'form': form})
        logging.warning("ERROR creating new application..")
        logging.error(form.errors)
        
    return render(request, 'application/new.html', context)        


    
