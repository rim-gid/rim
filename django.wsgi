# -*- coding: utf-8 -*-

import sys, os, os.path,  site 

os.environ["CELERY_LOADER"] = "django"

import djcelery
djcelery.setup_loader()

site.addsitedir(os.path.join(os.path.dirname(__file__), '..',
    '.env', 'lib', 'python2.6', 'site-packages'))

if not os.path.dirname(__file__) in sys.path[:1]: 
    sys.path.insert(0, os.path.dirname(__file__)) 
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings' 

from django.core.handlers.wsgi import WSGIHandler 
application = WSGIHandler()

