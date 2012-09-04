# -*- coding: utf-8 -*-
import sys, os, site
from django.conf import settings

PROJ_PATH = os.path.dirname(__file__)
site.addsitedir(os.path.join(PROJ_PATH, '..',
    '.env', 'lib', 'python2.6', 'site-packages'))
sys.path.append(PROJ_PATH)
sys.path.append(PROJ_PATH + '/../rim_version')

import project_params, project_local_params

os.environ['PYTHON_EGG_CACHE'] = '/usr/local/www/egg_cache'

ADMIN_MEDIA_ROOT = '/admin-media/'
ADMIN_MEDIA_PREFIX = '/admin-media/'

MP = project_params.AAA_SITE_PARAMS
MP['local'] = project_local_params.AAA_SITE_LOCAL_PARAMS

DEBUG = False
if "DEBUG" in MP['local']:
    if MP['local']['DEBUG']:
        DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Andrey', 'aa.veter@gmail.com'),
)

MANAGERS = ADMINS

PYTHON_EGG_CACHE = PROJ_PATH + ".python-eggs"

RIM_ADDRESSES = ['141.8.193.148', '141.8.193.142']
RIM_PASSES = ["udtufugeve", "gahaciicpi"]
if "TESTING" in MP['local']:
    if MP['local']['TESTING']:
        RIM_ADDRESSES = ['10.10.10.59', '10.10.10.7']
        RIM_PASSES = ["ceTNil", "ceTNil"]

# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = project_params.LANGUAGE_CODE

SITE_ID = project_params.SITE_ID

def get_my_address():
    k = SITE_ID - 1
    return RIM_ADDRESSES[k]

def get_pointed_address():
    if SITE_ID == 1:
        return RIM_ADDRESSES[1]
    else:
        return RIM_ADDRESSES[0]

def get_pointed_pass():
    if SITE_ID == 1:
        return RIM_PASSES[1]
    else:
        return RIM_PASSES[0]

def get_databases():
    local = {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'aaveter_0',
        'USER': 'aaveter_0',
        'PASSWORD': 'uR1zdiC7',
        'HOST': 'localhost',
        'PORT': '3306'
    }
    point = {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'aaveter_0',
        'USER': 'pointed',
        'PASSWORD': 'byd738ddu3289eud',
        'HOST': get_pointed_address(),
        'PORT': '3306'
    }
    if SITE_ID == 1:
        return point, local
    else:
        return local, point
        
default, point = get_databases()

DATABASES = {
    'default': default,
    'pointed': point
}

# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'Europe/Rome'

USE_I18N = True

MEDIA_ROOT = PROJ_PATH + '/rimgid/'
MEDIA_URL = '/rimgid/'

DEFAULT_CHARSET = 'UTF-8'

from project_params import *

SECRET_KEY = '4f_el$0#*3oyxaf9@#fhh*of6w(iumyev7-z_932@fcw*g)ets'

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
    'rimgid.articles.middleware.ArticleFallbackMiddleware',
    #'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'rimgid.urls'

TEMPLATE_DIRS = (
    PROJ_PATH + '/rimgid/templates',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.admin',
    'rimgid',
    'rimgid.articles',
    'rimgid.templatetags',
    'rimgid.added',
    'djcelery',
    'djkombu',
    'rimcelery',
)

import djcelery
djcelery.setup_loader()

CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"

BROKER_BACKEND = "djkombu.transport.DatabaseTransport"
