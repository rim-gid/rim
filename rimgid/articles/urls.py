# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from views import *

urlpatterns = patterns('',
    # общие страницы------------------:
    ('^/?$', get_page, {'url':''}),
    ('^/?(?P<url>\w+)?/?$', get_page),
    # общие страницы end------------------:
    
)

