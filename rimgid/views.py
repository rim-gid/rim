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
    mes_text += u"\nЭкскурсия: "+ ex + u"\nЖелаемая дата: " + date;
    mes_text += u"\nКомментарий: " + text;
    mes_text += u"\n\nЭто письмо сгенерировано автоматически. Для связи с клиентом используйте данные в тексте выше."
    mes_text += u"Если этот текст таких данных не содержит, значит у клиента возникли трудности с их вводом. Возможно он попробует отправить заказ повторно.";
    mes_text += u"\n\nС уважением, Ваш робот пересылки заказов"
    
    # -*- coding: utf-8
    #import os
    #import time
    # от кого и кому отправлять 
    #fromaddr = "iridium.toread@gmail.com"
    fromaddr = mail;
    toaddr = "aa.veter@gmail.com"
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
      rand_note = random.randint(0, len(notes_list)-1);
      note = notes_list[rand_note];
    if len(footer_list) > 0:
      rand_footer = random.randint(0, len(footer_list)-1);
      footer = footer_list[rand_footer];
    if len(shops_list) > 0:
      rand_shop = random.randint(0, len(shops_list)-1);
      shop = shops_list[rand_shop];
    if len(transport_list) > 0:
      rand_transport = random.randint(0, len(transport_list)-1);
      transport = transport_list[rand_transport];
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
    elif page_type == 'shops' :
      url = 'shops.html';
      excursion_list = Excursion.objects.all();
    elif page_type == 'fotos' :
      url = 'fotos.html';
      fotos_list = Fotos.objects.all();
      excursion_list = Excursion.objects.all();
    elif page_type == 'recomendations' :
      url = 'recomendations.html';
      recomendations_list = Recomendations.objects.all();
      excursion_list = Excursion.objects.all();
    elif page_type == "notes" :
      url = "notes.html";
      excursion_list = Excursion.objects.all();
    elif page_type == "translate" :
      url = "translate.html";
      datas = OlgaInfo.objects.all();
      
      data = datas[1];
      db_template = Template(data.hello_text);
      db_rez_template = Template('{% extends db_template %}');
      db_c = Context(locals());
      db_t = db_template.render(db_c);

      excursion_list = Excursion.objects.all();
    elif page_type == "italy" :
      url = "italy.html";
      excursion_list = Excursion.objects.all();
    return render_to_response(url, locals())

def excursion_order(request,ex,mail,text):
    rez = accounts_profile(request,ex,mail,text);
    return HttpResponse(str(rez), mimetype="text/html");

def excursion_page(request, num):
    #if request.needtosended is not None and request.needtosended = True:
      #return HttpResponseRedirect("/login/")
      
    footer_list = SiteFooter.objects.all();
    if len(footer_list) > 0:
      footer = footer_list[0];
    url = 'excursion.html';
    excursion_list = Excursion.objects.all();
    t_num = int(num)-1;
    ex_num = str(t_num);
    if num > 0 :
      if len(excursion_list) > t_num :
        excursion = excursion_list[t_num];
        db_template = Template(excursion.text_full);
        db_rez_template = Template('{% extends db_template %}');
        db_c = Context(locals());
        db_t = db_template.render(db_c);
        #t = Template('{% filter wordcount %}{% include "excursion_fulltext.html" %}{% endfilter %}');
        #c = Context(locals());
        #wordcount = int(t.render(c));
        #abcount = len(db_t);
    return render_to_response(url, locals())

def ex_list(request):
    url = 'ex_list.html';
    excursion_list = Excursion.objects.all();
    return render_to_response(url, locals())

def error404(request):
    url = '404.html';
    request_path = request.path;
    excursion_list = Excursion.objects.all();
    return render_to_response(url, locals())


    
#def border_radius(request):
#    url = 'border-radius.html';
#    return render_to_response(url, locals())

def get_css(request,name):
    url = "css/" + name + ".css";
    return render_to_response(url, locals())
    
def get_htc(request,name):
    url = settings.MEDIA_ROOT + "templates/htc/" + name + ".htc";
    ufile = open(url, "rb").read()
    return HttpResponse(ufile, mimetype="text/x-component")
    
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
    
def get_papka_jpg(request,papka,name):
    image_name = settings.MEDIA_ROOT + "images/" + papka + "/" + name + ".jpg";
    image_data = open(image_name, "rb").read()
    return HttpResponse(image_data, mimetype="image/jpg")
    
def get_ttf(request,name):
    image_name = settings.MEDIA_ROOT + "images/" + name + ".ttf";
    image_data = open(image_name, "rb").read()
    return HttpResponse(image_data, mimetype="image/ttf")
    
def get_pdf(request,name):
    image_name = settings.MEDIA_ROOT + "images/" + name + ".pdf";
    image_data = open(image_name, "rb").read()
    return HttpResponse(image_data, mimetype="image/pdf")


