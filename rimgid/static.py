# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404
from django.template import Template, Context
from django.shortcuts import render_to_response
from django.conf import settings
from django.contrib import auth
import datetime, random, os, time
from rimgid.forms import ContactForm

def get_css(request,name):
    f = "css/" + name + ".css"
    return render_to_response(f, locals())

def get_js(request,name):
    f = "js/" + name + ".js"
    return render_to_response(f, locals())
    
def get_from_wysiwyg(request,name,tp):
    url = settings.MEDIA_ROOT + "wysiwyg/" + name + "." + tp
    try:
      ufile = open(url, "rb").read()
    except:
      raise Http404('No %s matches the given query.' % url)
    
    if tp == "js":
      return HttpResponse(ufile, mimetype="text/javascript")
    elif tp == "css":
      return HttpResponse(ufile, mimetype="text/css")
    elif tp == "gif":
      return HttpResponse(ufile, mimetype="image/gif")
    else:
      raise Http404('No %s matches the given query.' % url)
      
    
def get_htc(request,name):
    url = settings.MEDIA_ROOT + "templates/htc/" + name + ".htc"
    ufile = open(url, "rb").read()
    return HttpResponse(ufile, mimetype="text/x-component")
    
def get_papka_jpg(request,papka,name):
    return get_image(request,papka+"/"+name,"jpg")

def get_papka_gif(request,papka,name):
    return get_image(request,papka+"/"+name,"gif")

def get_image(request,name,tp,papka):
    try:
      if len(papka) > 0:
        name = papka + "/" + name
    except TypeError:
      papka=""
    image_name = "images/" + name + "." + tp
    try:
      image_data = open(settings.MEDIA_ROOT+image_name, "rb").read()
    except IOError:
      try:
        image_data = open("rimgid/"+image_name, "rb").read()
      except:
        raise Http404('No %s matches the given query.' % ("rimgid/"+image_name))
    return HttpResponse(image_data, mimetype="image/"+tp)