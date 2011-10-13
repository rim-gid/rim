# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import Template, Context
import datetime
from django.shortcuts import render_to_response
from rimgid.books.models import *
from django.conf import settings

def robots(request):
    return render_to_response('robots.txt', locals())

def method_splitter(request, GET=None, POST=None):
    if request.method == 'GET' and GET is not None:
        return GET(request)
    elif request.method == 'POST' and POST is not None:
        return POST(request)
    raise Http404

def base_left_page(request, page_type='404'):
    notes_list = Note.objects.all();
    footer_list = SiteFooter.objects.all();
    shops_list = Shops.objects.all();
    transport_list = Transport.objects.all();
    if len(notes_list) > 0:
      note = notes_list[len(notes_list)-1];
    if len(footer_list) > 0:
      footer = footer_list[0];
    if len(shops_list) > 0:
      shop = shops_list[len(shops_list)-1];
    if len(transport_list) > 0:
      transport = transport_list[len(transport_list)-1];
    if page_type == 'main' :
      url = 'base_main.html';
      excursion_list = Excursion.objects.all();
    elif page_type == 'contacts' :
      url = 'base_contacts.html';
      contacts_list = Contacts.objects.all();
    elif page_type == 'transfer' :
      url = 'transfer.html';
      transfers_list = Transfer.objects.all();
      excursion_list = Excursion.objects.all();
    elif page_type == 'transport' :
      url = 'transport.html';
      excursion_list = Excursion.objects.all();
    elif page_type == 'recomendations' :
      url = 'recomendations.html';
      recomendations_list = Recomendations.objects.all();
      excursion_list = Excursion.objects.all();
    elif page_type == "notes" :
      url = "notes.html";
      excursion_list = Excursion.objects.all();
    return render_to_response(url, locals())

def excursion_page(request, num):
    footer_list = SiteFooter.objects.all();
    if len(footer_list) > 0:
      footer = footer_list[0];
    url = 'excursion.html';
    excursion_list = Excursion.objects.all();
    t_num = int(num)-1;
    if num > 0 :
      if len(excursion_list) > t_num :
        excursion = excursion_list[t_num];
    return render_to_response(url, locals())

def ex_list(request):
    url = 'ex_list.html';
    excursion_list = Excursion.objects.all();
    return render_to_response(url, locals())

def get_css(request,name):
    url = "css/" + name + ".css";
    return render_to_response(url, locals())
    
def get_png(request,name):
    image_name = settings.MEDIA_ROOT + "images/" + name + ".png";
#    image_name = "application/rimgid/images/" + name + ".png";
    image_data = open(image_name, "rb").read()
    return HttpResponse(image_data, mimetype="image/png")

def get_num_image_png(request,url,num):
    name = url + num;
    return get_png(request,name);
      
def get_num_image_jpg(request,url,num):
    name = url + num;
    return get_jpg(request,name);

def get_jpg(request,name):
    image_name = settings.MEDIA_ROOT + "images/" + name + ".jpg";
    image_data = open(image_name, "rb").read()
    return HttpResponse(image_data, mimetype="image/jpg")
    
def get_ttf(request,name):
    image_name = settings.MEDIA_ROOT + "images/" + name + ".ttf";
    image_data = open(image_name, "rb").read()
    return HttpResponse(image_data, mimetype="image/ttf")
    
 
