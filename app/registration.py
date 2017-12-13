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
from .models import Area
from .models import Person
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
from django.contrib import messages
from django.utils.translation import ugettext as _


def register(request):
    context={}
    return render(request, 'registration/registration_form.html', context)

def send_activation_email(user, request):
    current_site = get_current_site(request)
    message = render_to_string('registration/activation_email.html', {
        'user': user, 
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    email_to = ['{}'.format(user.email)]
    subject = settings.EMAIL_SIGN_UP_SUBJECT
    email_from = settings.EMAIL_SIGN_UP_FROM
    email_reply_to = settings.EMAIL_REPLY_TO
    email = EmailMessage(subject,message, email_from, email_to,reply_to=email_reply_to)

    if subject and message and email_from:
        try:
            logging.warning("sending sign up email to {}..".format(email_to))
            if email.send():
                return True
            else:
                logging.warning('The email could not be sent.')
        except BadHeaderError as e:
            logging.error("Invalid header found {}".format(e))
        except Exception as e:
            logging.error("Exception error: {}".format(e))
    
    return False


@transaction.atomic    
def complete(request):
    context = {}

    if request.method != 'POST':
        logging.warning("Attempt to create account without using post method as it should be")
        return redirect('login')
    
    form = SignupForm(request.POST)
    if form.is_valid():
        try:
            sid = transaction.savepoint()
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            person = Person(user=user)
            person.save()
        except Exception as e:
            logging.error('ERROR Exception: %s', e)
            transaction.savepoint_rollback( sid )
            context.update({'form': form})
            messages.warning(request, _('registration_not_found'))
            return render(request, 'registration/registration_form.html', context)
            
        transaction.savepoint_commit( sid )
        context.update({'email': user.email})
        if send_activation_email(user, request):
            return render(request, 'registration/registration_complete.html', context)
        else:
            user.delete()
            return render(request, 'registration/registration_error.html', context)
    else:
        context.update({'form': form})
        logging.warning("Invalid user form, errors: %s" % form.errors)
        return render(request, 'registration/registration_form.html', context)

    
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        logging.warning('Activating {} user with token {}'.format(user, token))
        user.is_active = True
        user.save()
        return render(request, 'registration/activation_complete.html')
    else:
        logging.error('Error activating {} user with token {}'.format(user, token))
        return render(request, 'registration/activate.html')



    

