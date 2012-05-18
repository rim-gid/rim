# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import Template, Context
import datetime
from django.shortcuts import render_to_response
from rimgid.books.models import *
from django.conf import settings
import random

import os
from smtplib import SMTP
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import Encoders
import time
from django.contrib import auth

from django.core.mail import send_mail
from django.shortcuts import render_to_response
from rimgid.forms import ContactForm

def accounts_profile(request,name,ex,mail,text,date):
    mes_text = u"Вам отправили заказ. Детали заказа смотрите ниже:\n\n";
    mes_text += u"Имя: " + name + u"\nОбратный e-mail: " + mail;
    try:
      mes_text += u"\nЭкскурсия: "+ ex 
    except:
      ex= u"не задано" 
      mes_text += u"\nЭкскурсия: "+ ex 
    try:
      mes_text += u"\nЖелаемая дата: " + date
    except:
      date = u"не задано"
      mes_text += u"\nЖелаемая дата: " + date
      
    mes_text += u"\nКомментарий: " + text;
    mes_text += u"\n\nЭто письмо сгенерировано автоматически. Для связи с клиентом используйте данные в тексте выше."
    mes_text += u"Если этот текст таких данных не содержит, значит у клиента возникли трудности с их вводом. Возможно он попробует отправить заказ повторно.";
    mes_text += u"\n\nС уважением, Ваш робот пересылки заказов"
    try:
      mes_text += "\n---server version: "+settings.AAA_SITE_PARAMS.site_version
    except:
      mes_text += "\n---server version: not getted"
    
    # -*- coding: utf-8
    #import os
    #import time
    # от кого и кому отправлять 
    #fromaddr = "iridium.toread@gmail.com"
    fromaddr = mail;
    toaddr = "aa.veter@gmail.com;oan_75@mail.ru;"
    # дамп БД и медиафайлы сжимаем в файл buckup.tar.gz
    #os.system("mysqldump -u [пользователь] --password=[пароль] [БД] [таблица1] [таблица2]> dump.sql")
    #os.system("tar -zcf backup.tar.gz dump.sql [путь к каталогу с медиа файлами]")
    # создаем почтовое сообщение
    msg = MIMEMultipart()
    # заполняем поля отправителя, адресата и тему сообщения
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = u'заказ ' + date + " " + ex + " " + name + " " + mail;
    # текстовая часть сообщения (не забываем указать кодировку)
    msg.attach(MIMEText(mes_text, "plain", "utf-8"))
    # прикрепляем файл backup.tar.gz к почтовому сообщению
    #att = MIMEBase('application', 'octet-stream')
    #att.set_payload(open("/home/git/ttt", "rb").read())
    #att.set_payload(mes_text)
    
    #Encoders.encode_base64(att)
    #att.add_header('Content-Disposition', 'attachment; filename="README"')
    #msg.attach(att)
    
    #return "OK"
    # соединяемся с почтовым сервером и выполняем авторизацию
    server = SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login("gid.po.rimu", "f2y0l0h10tqhfgf")
    # отправляем сформированное сообщение, после чего выходим
    server.sendmail(fromaddr, toaddr, msg.as_string())
    server.quit()
    #os.system("/home/git/test")
    return "OK"

def contact_form(request,ex=""):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            #send_mail(
            #    cd['subject'],
            #    cd['message'],
            #    cd.get('email', 'noreply@example.com'),
            #    ['siteowner@example.com'],
            #)
            #accounts_profile(request,cd.get('email', 'noreply@example.com'),cd.get('email', 'noreply@example.com'),cd.get('email', 'noreply@example.com'))
            order_ok = "True";
            mail = cd.get('email', '-');
            date = cd.get('subject', '-');
            text = cd.get('message', '-');
            name = cd.get('name', '-');
            #accounts_profile(request,"name","ex","mail","text","date");
            #return HttpResponse(ex, mimetype="text/html");
            if accounts_profile(request,name,ex,mail,text,date) == "OK":
              return HttpResponse(u"Спасибо за заказ! Я Вам отвечу в ближайшее время (до нескольких дней).", mimetype="text/html");
            er_str = u"Ошибка отправки заказа!<br> Возможно это технические неполадки сайта. ";
            er_str += u"Если ошибка повторяется, попробуйте отправить заказ вручную на мою почту oan_75@mail.ru ";
            er_str += u"или связаться со мной любым удобным для Вас способом.<br>Мои контакты перечислены на странице gid-rim.com/contacts";
            return HttpResponse(er_str, mimetype="text/html");
    else:
        form = ContactForm(
            #initial={'subject': 'I love your site!'}
        )
    return render_to_response('contact_form.html', locals())

def robots(request):
    return render_to_response('robots.txt', locals())
    
def yandex_61b9f126eb948082_txt(request):
    return render_to_response('yandex_61b9f126eb948082.txt', locals())
    
def html_1be09f3f8a74_html(request):
    return render_to_response('1be09f3f8a74.html', locals())

def method_splitter(request, GET=None, POST=None):
    if request.method == 'GET' and GET is not None:
        return GET(request)
    elif request.method == 'POST' and POST is not None:
        return POST(request)
    raise Http404

def edit_excursions(request):
    excursion_list = Excursion.objects.all();
    return render_to_response('edit_excursions.html',locals())

def jseditor(request):
    return render_to_response('jseditor.html',locals())

def get_main_params():
    mp = settings.AAA_SITE_PARAMS
    mp['local']=settings.AAA_SITE_LOCAL_PARAMS
    return mp

def excursion_page(request, num):
    mp = get_main_params()
    footer_list = SiteFooter.objects.all()
    if len(footer_list) > 0:
      footer = footer_list[0]
    url = 'excursion.html'
    excursion_list = Excursion.objects.all()
    t_num = int(num)-1;
    ex_num = str(t_num);
    if num > 0 :
      if len(excursion_list) > t_num:
        excursion = excursion_list[t_num]
        db_template = Template(excursion.text_full)
        db_rez_template = Template('{% extends db_template %}')
        db_c = Context(locals())
        db_t = db_template.render(db_c)
    return render_to_response(url, locals())

# рендерит все заметки выбранной таблицы
def renderNotesText(objs):
    datas = objs.objects.all()
    i = 0
    for data in datas:
      db_template = Template(data.text)
      data.text = Template('{% extends db_template %}').render(Context(locals()))
      i += 1
    return datas
    
# рендерит конкретную заметку
def renderNote(note):
    if note:
      db_template = Template(note.text)
      note.text = Template('{% extends db_template %}').render(Context(locals()))
      return note
    return note
    
def get_page(request, page_type='404'):
    mp = get_main_params()

    if page_type == 'main':
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
    elif page_type == 'recomendations':
      recomendations_list = renderNotesText(Recomendations)
    elif page_type == "translate" :
      datas = OlgaInfo.objects.all()
      data = datas[1]
      db_template = Template(data.hello_text)
      db_rez_template = Template('{% extends db_template %}')
      db_c = Context(locals())
      db_t = db_template.render(db_c)
    elif page_type == "notes" :
      content_name = u'Новости'
      content_no = u'Пока нет ни одной новости'
      content_list = renderNotesText(Note)
    elif page_type == "shops" :
      content_name = u'Магазины'
      content_no = u'Пока нет ни одной заметки про магазины'
      content_list = renderNotesText(Shops)
      page_type = "notes"
    elif page_type == "transport" :
      content_name = u'Транспорт'
      content_no = u'Пока нет ни одной заметки про транспорт'
      content_list = renderNotesText(Transport)
      page_type = "notes"
    
    try:
      url = page_type+".html"
      excursion_list = Excursion.objects.all()
      return render_to_response(url, locals())
    except:
      return error404(request)

def excursion_order(request,ex,mail,text):
    rez = accounts_profile(request,ex,mail,text);
    return HttpResponse(str(rez), mimetype="text/html");

def ex_list(request):
    url = 'ex_list.html';
    excursion_list = Excursion.objects.all();
    return render_to_response(url, locals())

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
    
def test(request):
    data="<?xml version='1.0' encoding='utf-8'?>"
    data+="<data>"
    try:
      main = SiteParam.objects.get(name="main")
      values = main.value.split(";")
      for val in values:
	vv = val.split("=")
	if len(vv) > 1:
	  data += "<value id='"+vv[0]+"'>" +vv[1]+ "</value>"
    except SiteParam.DoesNotExist:
      return error404(request)
    data+="</data>"
    return HttpResponse(data, mimetype="text/xml")
    xargs = main.value.split("&")
    xa_len = len(xargs)
    if xa_len < 1:
      return HttpResponse("ERROR*xa_len < 1 in: "+args, mimetype="text/html");
    return HttpResponse("ERROR*xa_len < 1 in: "+args, mimetype="text/html");
#def border_radius(request):
#    url = 'border-radius.html';
#    return render_to_response(url, locals())

def get_css(request,name):
    url = "css/" + name + ".css";
    return render_to_response(url, locals())

def get_js(request,name):
    url = "js/" + name + ".js";
    return render_to_response(url, locals())
    
def get_htc(request,name):
    url = settings.MEDIA_ROOT + "templates/htc/" + name + ".htc";
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
    image_name = "images/" + name + "." + tp;
    try:
      image_data = open(settings.MEDIA_ROOT+image_name, "rb").read()
    except IOError:
      image_data = open("rimgid/"+image_name, "rb").read()
    return HttpResponse(image_data, mimetype="image/"+tp)
