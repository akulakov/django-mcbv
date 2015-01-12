""" Django settings for dbe project.  """

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from os.path import join as pjoin
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shared',
    'issues',
    'blog',
    'bombquiz',
    'forum',
    'portfolio',
    'questionnaire',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_DIRS = (
     os.path.join(BASE_DIR, "templates"),
     os.path.join(BASE_DIR, "templates", "issues"),
     os.path.join(BASE_DIR, "templates", "blog"),
     os.path.join(BASE_DIR, "templates", "bombquiz"),
     os.path.join(BASE_DIR, "templates", "forum"),
     os.path.join(BASE_DIR, "templates", "portfolio"),
     os.path.join(BASE_DIR, "templates", "questionnaire"),
     )

ROOT_URLCONF = 'dbe.urls'

WSGI_APPLICATION = 'dbe.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

MEDIA_URL = '/media/'
MEDIA_ROOT = pjoin(BASE_DIR, "media")
STATIC_URL = '/static/'
STATICFILES_DIRS = (
                    pjoin(BASE_DIR, "static"),
                    )

try:
    from local_settings import *
except:
    pass
