# -*- coding: utf-8 -*-
import os, sys, site
sys.path.insert(0, os.path.dirname(__file__))
#site.addsitedir('/home/httpd/env/djbookru/lib/python2.6/sitepackages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
