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
from .forms import ResetPasswordForm
from .forms import DefinePasswordForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.core.exceptions import MultipleObjectsReturned
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
    current_site = get_current_site(request)
    message = render_to_string('email_sign_up.html', {
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



def send_reset_password_email(user, request):
    current_site = get_current_site(request)
    message = render_to_string('email_reset_password.html', {
        'user': user, 
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    email_to = ['{}'.format(user.email)]
    subject = settings.EMAIL_RESET_PASSWORD_SUBJECT
    email_from = settings.EMAIL_RESET_PASSWORD_FROM
    email_reply_to = settings.EMAIL_REPLY_TO
    email = EmailMessage(subject,message, email_from, email_to,reply_to=email_reply_to)
    
    if subject and message and email_from:
        try:
            logging.warning("sending reset password email to {}..".format(email_to))
            if email.send():
                return True
            else:
                logging.warning('The email could not be sent.')
        except BadHeaderError as e:
            logging.error("Invalid header found {}".format(e))
        except Exception as e:
            logging.error("Exception error: {}".format(e))
    
    return False


def send_password_changed_email(user, request):
    current_site = get_current_site(request)
    message = render_to_string('email_password_changed.html', {
        'user': user, 
        'domain': current_site.domain,
    })
    email_to = ['{}'.format(user.email)]
    subject = settings.EMAIL_PASSWORD_CHANGED_SUBJECT
    email_from = settings.EMAIL_PASSWORD_CHANGED_FROM
    email_reply_to = settings.EMAIL_REPLY_TO
    email = EmailMessage(subject,message, email_from, email_to,reply_to=email_reply_to)

    if subject and message and email_from:
        try:
            logging.warning("sending password changed email to {}..".format(email_to))
            if email.send():
                return True
            else:
                logging.warning('The email could not be sent.')
        except BadHeaderError as e:
            logging.error("Invalid header found {}".format(e))
        except Exception as e:
            logging.error("Exception error: {}".format(e))
    
    return False


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
        context.update({'email': user.email})
        if send_activation_email(user, request):
            return render(request, 'msg_email_sent.html', context)
        else:
            user.delete()
            return render(request, 'msg_email_not_sent.html', context)
    else:
        context.update({'form': form})
        logging.warning("Invalid user form, errors: %s" % form.errors)
        return render(request, 'sign_up.html', context)

    

            

def account_forgot_password(request):
    context={}
    return render(request, 'forgot_password.html', context)


def account_reset_password(request):
    context = {}

    if request.method != 'POST':
        logging.warning("Attempt to reset password without using post method as it should be")
        return redirect('login')
    
    form = ResetPasswordForm(request.POST)
    if form.is_valid():
        user_email = form.cleaned_data['email']
        user = None
        try:
            user = User.objects.get(email=user_email)
        except(User.DoesNotExist):
            logging.warning("Error when restoring password for a user whose email was not found")
        except(MultipleObjectsReturned):
            logging.warning("Several users were found with the same email")
        except Exception as e:
            logging.error(e)
            
        if user is not None and send_reset_password_email(user, request):
            context.update({'email': user.email})
            return render(request, 'msg_reset_password_email_sent.html', context)
        else:
            return render(request, 'msg_reset_password_email_not_sent.html') 
    else:
        context.update({'form': form})
        logging.warning("Invalid reset password form, errors: %s" % form.errors)
        return render(request, 'forgot_password.html', context)


def account_define_password(request, uidb64, token):
    context = {'uidb64': uidb64, 'token': token}
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        logging.error('In the attempt to define new password with incorrect token url')
        return redirect('login')

    return render(request, 'confirm_reset_password.html', context)


def account_activate_password(request, uidb64, token):
    context = {'uidb64': uidb64, 'token': token}    
    user = None    
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(User.DoesNotExist):
        logging.warning("Error when restoring password for a user whose email was not found")
    except(MultipleObjectsReturned):
        logging.warning("Several users were found with the same email")
    except Exception as e:
        logging.error(e)

    if user is not None and account_activation_token.check_token(user, token):
        logging.warning('Activating new password {} user with token {}'.format(user, token))

        form =  DefinePasswordForm(request.POST)
        if form.is_valid():
            try:
                new_password = form.cleaned_data['password1']
                user.set_password(new_password)
                user.save()
                logging.warning("password changed for user {}".format(user))
                send_password_changed_email(user,request)
                return render(request, 'msg_confirm_reset_password.html')
            except Exception, e:
                logging.warning("ERROR, password not changed")
                return render(request, 'msg_confirm_reset_password_error.html')
        else:
            context.update({'form': form})
            logging.warning("Invalid confirm reset password form, errors: %s" % form.errors)
            return render(request, 'confirm_reset_password.html', context)
    else:
        logging.error('Error activating {} user with token {}'.format(user, token))
        return redirect('login')
    
