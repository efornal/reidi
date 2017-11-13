# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


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


