"""
Django settings for proj_issues project.
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_91vd5tl+)&-j-=h8p6m4w*!dtcj=z&_!pp75&f%f)spyt1qpa'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'issues',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'proj_issues.urls'
WSGI_APPLICATION = 'proj_issues.wsgi.application'

LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'UTC'
USE_I18N      = True
USE_L10N      = True
USE_TZ        = True
STATIC_ROOT   = BASE_DIR + "/issues/static/"
STATIC_URL    = '/static/'
MEDIA_ROOT    = BASE_DIR + "/media/"
MEDIA_URL     = "/media/"

# STATICFILES_DIRS = (
    # os.path.join(BASE_DIR, "static"),
# )

TEMPLATE_DIRS = [
                 BASE_DIR + "/templates/",
                 BASE_DIR + "/templates/issues/",
                 ]

TEMPLATE_CONTEXT_PROCESSORS = \
    ("django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "issues.views.context_processor",
     )

# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_BACKEND   = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH   = '/tmp/emails/'
EMAIL_BACKEND     = 'django.core.mail.backends.console.EmailBackend'
TEST_NOTIFY       = False       # send notification email to originating user (for testing only)
BOLD_LABELS       = False       # bold labels in issue form

SHOW_PROGRESS_BAR = True
SEARCH_ON         = True        # search in admin
SPECIAL_STATUS_CODES = dict(
                            open    = "1 - open",
                            done    = "4 - done",
                            wontfix = "5 - won't fix",
                            )

try:
    from local_settings import *
except Exception, e:
    print("ignoring exception..")
    print(e)
