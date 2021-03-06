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
from .forms import EditUserForm
from .forms import EditPersonForm
from .models import Domain
from .models import Person
from .models import DocumentType
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.core.exceptions import MultipleObjectsReturned
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import ugettext as _

def logout_message(request):
    context={}
    return render(request, 'msg_logout.html', context)


@login_required
def edit(request):
    try:
        user = request.user
        person = Person.objects.get(user=user)
    except(Person.DoesNotExist):
        try:
            person = Person(user=user)
            person.save()
            logging.warning('Created {} person corresponding to the user {}'
                            .format(person,user))
        except Exception as e:
            logging.error('Exception: creating the person to the user. %s', e)
    except Exception as e:
        logging.error('Exception: looking for the person and corresponding user. %s', e)
        return redirect('index')
        
    form = EditUserForm(instance=user)
    person_form = EditPersonForm(instance=person)
    
    context={'form': form,
             'person_form': person_form,
             'doc_types': DocumentType.objects.all()}
    return render(request, 'auth/edit.html', context)


@login_required
def save(request):
    context={}
    user = request.user
    person = Person.objects.get(user=user)
    form = EditUserForm(request.POST,instance=user)
    person_form = EditPersonForm(request.POST,instance=person)
    update_fields_person = ['telephone_number','document_type','document_number']
    update_fields_user = ['first_name', 'last_name', 'email']
    if form.is_valid():
        if person_form.is_valid():
            person_form.instance.save(update_fields=update_fields_person)
            form.instance.save(update_fields=update_fields_user)
            messages.info(request, _('changes_saved'))
        else:
            logging.warning ("Error to update person {}".format(person_form.errors))
    else:
        logging.warning ("Error to update user {}".format(form.errors))

    context.update({'form': form,
                    'person_form': person_form})
    return render(request, 'auth/edit.html', context)



def send_reset_password_email(user, request):
    current_site = get_current_site(request)
    message = render_to_string('auth/email_reset_password.html', {
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
    message = render_to_string('auth/email_reset_password_done.html', {
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

            

def password_reset(request):
    context={}
    return render(request, 'auth/password_reset.html', context)


def password_reset_complete(request):
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
            return render(request, 'auth/password_reset_done_sent.html', context)
        else:
            return render(request, 'auth/password_reset_done_not_sent.html') 
    else:
        context.update({'form': form})
        logging.warning("Invalid reset password form, errors: %s" % form.errors)
        return render(request, 'auth/password_reset.html', context)


def password_reset_confirm(request, uidb64, token):
    context = {'uidb64': uidb64, 'token': token}
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        logging.error('In the attempt to define new password with incorrect token url')
        return redirect('login')

    return render(request, 'auth/password_reset_confirm.html', context)


def password_change(request, uidb64, token):
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
                return render(request, 'auth/password_reset_complete.html')
            except Exception, e:
                logging.warning("ERROR, password not changed. {}".format(e))
                return render(request, 'auth/password_reset_error.html')
        else:
            context.update({'form': form})
            logging.warning("Invalid confirm reset password form, errors: %s" % form.errors)
            return render(request, 'confirm_reset_password.html', context)
    else:
        logging.error('Error activating {} user with token {}'.format(user, token))
        return redirect('login')
    
