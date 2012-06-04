# -*- coding: utf-8 -*-
# Django settings for application project.

import sys
sys.path.append('/usr/local/www/rim')
sys.path.append('/usr/local/www/rim_version')
sys.path.append('../rim_version')

import os
os.environ['PYTHON_EGG_CACHE'] = '/usr/local/www/egg_cache'

ADMIN_MEDIA_ROOT = '/admin-media/'
ADMIN_MEDIA_PREFIX = '/admin-media/'

from project_local_params import *

from django.conf import settings

def get_main_params():
    mp = settings.AAA_SITE_PARAMS
    mp['local']=settings.AAA_SITE_LOCAL_PARAMS
    return mp

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Andrey', 'aa.veter@gmail.com'),
)

MANAGERS = ADMINS

PYTHON_EGG_CACHE = "/usr/local/www/rim/.python-eggs"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'aaveter_0',
        'USER': 'aaveter_0',
        'PASSWORD': 'uR1zdiC7',
        'HOST': 'localhost',
        'PORT': '3306'
    }
}

DATABASE_ENGINE = 'django.db.backends.mysql'          # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'aaveter_0'             # Or path to database file if using sqlite3.
DATABASE_USER = 'aaveter_0'             # Not used with sqlite3.
DATABASE_PASSWORD = 'uR1zdiC7'         # Not used with sqlite3.
DATABASE_HOST = 'localhost'             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = '3306'             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Rome'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ru-RU'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
#MEDIA_ROOT = '/home/a/aaveter/public_html///rim/rimgid/'
MEDIA_ROOT = '/usr/local/www/rim/rimgid/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/rimgid/'

DEFAULT_CHARSET = 'utf8'

from project_params import *

#STATIC = '/home/a/aaveter/public_html///rim/rimgid/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
#ADMIN_MEDIA_PREFIX = '/admin_media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '4f_el$0#*3oyxaf9@#fhh*of6w(iumyev7-z_932@fcw*g)ets'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    #'django.template.loaders.filesystem.load_template_source',
    #'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'rimgid.urls'

TEMPLATE_DIRS = (
    '/usr/local/www/rim/rimgid/templates',
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'rimgid',
    'rimgid.books',
)