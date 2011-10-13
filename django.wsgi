#import os, sys
#sys.path.append('/var/lib/python-support/python2.6/django')
#sys.path.append('/usr/local/django/trunk/django') 
#sys.path.append('/usr/local/www/rim') 

#os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

#import django.core.handlers.wsgi
#application = django.core.handlers.wsgi.WSGIHandler()



import sys
import os
import os.path
 
sys.path.insert(0, os.path.dirname(__file__))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
 
from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
