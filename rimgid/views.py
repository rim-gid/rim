# -*- coding: utf-8 -*-
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
#from rimgid.articles.models import fill_excursions


def method_splitter(request, GET=None, POST=None):
    if request.method == 'GET' and GET is not None:
        return GET(request)
    elif request.method == 'POST' and POST is not None:
        return POST(request)
    raise Http404

def excursion_page(request, num):
    mp = get_main_params()
    footer_list = SiteFooter.objects.all()
    if len(footer_list) > 0:
      footer = footer_list[0]
    url = 'excursion.html'
    excursion_list = Excursion.objects.all()  
      
    t_num = int(num)-1;
    ex_num = str(t_num);
    tmp1 = mp['page_title']
    tmp2 = mp['page_keywords']
    if num > 0 :
      if len(excursion_list) > t_num:
        excursion = excursion_list[t_num]
        if excursion.special != 0:
          mp['page_title'] = excursion.special
          mp['page_keywords'] = excursion.special
        db_template = Template(excursion.text_full)
        db_rez_template = Template('{% extends db_template %}')
        db_c = Context(locals())
        db_t = db_template.render(db_c)
    rtr = render_to_response(url, locals())
    mp['page_title'] = tmp1
    mp['page_keywords'] = tmp2
    return rtr
    
def get_page(request, page_type='404'):
    mp = get_main_params()

    if page_type == 'main':
      
      try:
        if mp['owner_maintext_rendered'] != True:
          mp['owner_maintext'] = renderText(mp['owner_maintext'])
          mp['owner_maintext_rendered'] = True
      except:    
        mp['owner_maintext_rendered'] = True
        mp['owner_maintext'] = renderText(mp['owner_maintext'])
      
      try:
        notes_count = Note.objects.all().count()
        rand_note = random.randint(0, notes_count-1)
        note = renderNote(Note.objects.all()[rand_note])
        
        shops_count = Shops.objects.all().count()
        rand_shop = random.randint(0, shops_count-1)
        shop = renderNote(Shops.objects.all()[rand_shop])
        
        transport_count = Transport.objects.all().count()
        rand_transport = random.randint(0, transport_count-1)
        transport = renderNote(Transport.objects.all()[rand_transport])
      except:
        notes_error=True
    elif page_type == 'contacts':
      contacts_list = Contacts.objects.all()
    elif page_type == 'transfer':
      transfers_list = renderNotesText(Transfer)
    elif page_type == 'fotos':
      fotos_list = Fotos.objects.all()
    elif page_type == 'reccomendations':
      reccomendations_list = renderNotesText(Reccomendations)
    elif page_type == "translate" :
      datas = OlgaInfo.objects.all()
      data = datas[1]
      db_template = Template(data.hello_text)
      db_rez_template = Template('{% extends db_template %}')
      db_c = Context(locals())
      db_t = db_template.render(db_c)
    elif page_type == "notes" :
      content_name = mp['content_name_notes']
      content_no = mp['content_name_notes_no']
      content_list = renderNotesText(Note)
    elif page_type == "shops" :
      content_name = mp['content_name_shops']
      content_no = mp['content_name_shops_no']
      content_list = renderNotesText(Shops)
      page_type = "notes"
    elif page_type == "hotels" :
      content_name = mp['content_name_hotels']
      content_no = mp['content_name_hotels_no']
      content_list = renderNotesText(Hotels)
      page_type = "notes"
    elif page_type == "flights" :
      content_name = mp['content_name_flights']
      content_no = mp['content_name_flights_no']
      content_list = renderNotesText(Flights)
      page_type = "notes"
    elif page_type == "restaurants" :
      content_name = mp['content_name_restaurants']
      content_no = mp['content_name_restaurants_no']
      content_list = renderNotesText(Restaurants)
      page_type = "notes"
    elif page_type == "transport" :
      content_name = mp['content_name_transport']
      content_no = mp['content_name_transport_no']
      content_list = renderNotesText(Transport)
      page_type = "notes"
    
    try:
      url = page_type+".html"
      excursion_list = Excursion.objects.all()
      return render_to_response(url, locals())
    except:
      return error404(request)

def error404(request):
    mp = get_main_params()
    url = '404.html';
    request_path = request.path;
    excursion_list = Excursion.objects.all();
    return render_to_response(url, locals())

def about_pages(request, page):
    try:
        return direct_to_template(request, template="about/%s.html" % page)
    except TemplateDoesNotExist:
        raise Http404()
    



