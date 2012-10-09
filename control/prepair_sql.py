# -*- coding: utf-8 -*-
"""
from django.http import HttpResponse
from django.template import Template, Context
from django.shortcuts import render_to_response
from django.conf import settings
from django.contrib import auth
import datetime, random, os, time
from rimgid.books.models import *
from rimgid.views_order import *
from rimgid.views_yandex import *
from rimgid.views_render import *
from rimgid.views_static import *
from settings import get_main_params

#from django.core.mail import send_mail
from django.shortcuts import render_to_response
from rimgid.forms import ContactForm
from rimgid.articles.models import fill_excursions
"""

finded = False

def try_line(s):
    global finded
    if finded:
        if "--" in s:
            finded = False
            return s
        else:
            return ""
    if "DROP TABLE" in s:
        finded = True
        return ""
    else:
        return s

f = open("bf.sql")
w = open("bf_new.sql", "w")
lines = (t for t in f)
no_drops = (try_line(t) for t in lines)
#for n in no_drops:
#  w.write(n),
w.writelines(no_drops)