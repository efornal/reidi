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
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage



def set_language(request, lang='es'):
    if 'lang' in request.GET:
        lang = request.GET['lang']
    translation.activate(lang)
    request.session[translation.LANGUAGE_SESSION_KEY] = lang
    logging.info("Language changed by the user to '{}'".format(lang))
    return redirect('index')


@login_required
def index(request):
    context={}
    return render(request, 'index.html', context)



def account_sign_up(request):
    context={}
    return render(request, 'sign_up.html', context)


def logout_message(request):
    context={}
    return render(request, 'msg_logout.html', context)


def send_activation_email(user, request):
    email_sent = False
    current_site = get_current_site(request)
    message = render_to_string('email_sign_up.html', {
        'user': user, 
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    subject = settings.EMAIL_SUBJECT
    from_email = settings.EMAIL_FROM
    email_to = ['{}'.format(user.email)]
    
    if subject and message and from_email:
        try:
            logging.warning("sending email to {}..".format(email_to))
            if send_mail(subject, message, from_email, email_to):
                email_sent = True
            else:
                logging.warning('The email could not be sent.')
        except BadHeaderError as e:
            logging.error("Invalid header found {}".format(e))
        except Exception as e:
            logging.error("Exception error: {}".format(e))
    
    return email_sent


def account_activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        logging.warning('Activating {} user with token {}'.format(user, token))
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'msg_wellcome.html')
    else:
        logging.error('Error activating {} user with token {}'.format(user, token))
        return redirect('login')

    
def account_create(request):
    context = {}

    if request.method != 'POST':
        logging.warning("Attempt to create account without using post method as it should be")
        return redirect('login')
    
    form = SignupForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        
        if send_activation_email(user, request):
            return render(request, 'msg_email_sent.html')
        else:
            return render(request, 'msg_email_not_sent.html') 
    else:
        context.update({'form': form})
        logging.warning("Invalid user form, errors: %s" % form.errors)
        return render(request, 'sign_up.html', context)
        

            

