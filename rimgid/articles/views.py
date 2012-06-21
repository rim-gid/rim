# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import Template, Context
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
