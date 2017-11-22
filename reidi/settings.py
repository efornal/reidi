# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""
Django settings for reidi project.

Generated by 'django-admin startproject' using Django 1.11.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from django.utils.translation import ugettext_lazy as _


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPLICATION_NAME= "Reidi"
APPLICATION_DESC= "Subdomains requests"


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'y)$965=y74_0=nk#)6vmirjcg5d^w-*nu!nf(_w3a^1$3_@3)7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# =================================\
# email configuration server
EMAIL_HOST='correo.intranet'
EMAIL_PORT=25
EMAIL_HOST_PASSWORD=''
EMAIL_HOST_USER=''
# email configuration application
EMAIL_FROM = 'noreply@rectorado.unl.edu.ar'
EMAIL_SUBJECT = 'Solicitud de cuenta'
# =================================/

# Application definition

INSTALLED_APPS = [
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'jquery',
    'jquery_ui',
    'bootstrap_ui',
    'django_extensions',
    'bootstrap_themes',
    'app',
]
MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'app.middleware.ForceLangMiddleware',
]

ROOT_URLCONF = 'reidi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': True,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'reidi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'reidi_db',
        'USER': 'reidi_user',
        'PASSWORD': 'user',
        'PORT': '5432',
        'HOST': 'localhost',
    },
    'reidi_owner': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'reidi_db',
        'USER': 'reidi_owner',
        'PASSWORD': 'owner',
        'PORT': '5432',
        'HOST': 'localhost',
    },
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/


STATIC_URL = '/static/'

LANGUAGE_CODE = 'es'

LANGUAGES = (
  ('es', _('Spanish')),
  ('en', _('English')),
)

LOCALE_PATHS = (
     BASE_DIR + '/locale', )

TIME_ZONE = 'America/Argentina/Buenos_Aires'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_CHARSET = 'utf-8'

LOGIN_URL='/app/login/'

LOGIN_REDIRECT_URL = '/'

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

# django configuration
SUIT_CONFIG = {
    'ADMIN_NAME': APPLICATION_NAME
}
