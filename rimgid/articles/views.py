# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import Template, Context
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.conf import settings
from django.contrib import auth
import datetime, random, os, time
from rimgid.articles.models import *

def method_splitter(request, GET=None, POST=None):
    if request.method == 'GET' and GET is not None:
        return GET(request)
    elif request.method == 'POST' and POST is not None:
        return POST(request)
    raise Http404

def get_page(request, url='404'):
    pass


#from django.contrib.flatpages.models import FlatPage
from models import Article
from django.template import loader, RequestContext
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.conf import settings
from django.core.xheaders import populate_xheaders
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_protect

from django.contrib.flatpages.views import render_flatpage

DEFAULT_TEMPLATE = 'flatpages/default.html'

def article(request, url):
    """
    метод используется для использования вместо объекта FlatPage объекта Article
    """
    if not url.endswith('/') and settings.APPEND_SLASH:
        return HttpResponseRedirect("%s/" % request.path)
    if not url.startswith('/'):
        url = "/" + url
    #try:
    f = get_object_or_404(Article, url__exact=url, sites__id__exact=settings.SITE_ID)
    if f.is_only_in_list():
        raise Http404('No %s matches the given query.' % f.url)
    #except MultipleObjectsReturned:    
    return render_flatpage(request, f)
    
def file_text(template):
    t = get_template(template)
    return t.render(Context({}))