# -*- coding: utf-8
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

from django.template import RequestContext
from templatetags.project_options import get_project_option

def excursion_order(request,ex,mail,text):
    """
    Запрос отправки заказа
    """
    rez = accounts_profile(request,ex,mail,text);
    return HttpResponse(str(rez), mimetype="text/html")

def contact_form(request,ex=""):
    """
    Выдача формы контактов
    """
    if request.method == 'POST':
        #mp = get_main_params()
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            order_ok = "True";
            mail = cd.get('email', '-');
            date = cd.get('subject', '-');
            text = cd.get('message', '-');
            name = cd.get('name', '-');
            if send_order(request,name,ex,mail,text,date) == "OK":
                return HttpResponse(get_project_option('msg_thx'), mimetype="text/html")
            er_str = get_project_option('msg_error')
            er_str += get_project_option('msg_error_repeat')
            er_str += get_project_option('msg_error_contacts')
            return HttpResponse(er_str, mimetype="text/html")
    else:
        form = ContactForm()
    data = { 
        'form': form
    }
    return render_to_response( 'contact_form.html', data,
        context_instance=RequestContext(request))

def send_order(request,name,ex,mail,text,date):
    """
    Отправка заказа
    """
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
      mes_text += "\n---server version: "+settings.SITE_ID
    except:
      mes_text += "\n---server version: not getted"
    
    # от кого и кому отправлять 
    #fromaddr = "iridium.toread@gmail.com"
    fromaddr = mail;
    toaddr = "aa.veter@gmail.com;oan_75@mail.ru;"
    msg = MIMEMultipart()
    # заполняем поля отправителя, адресата и тему сообщения
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = u'заказ ' + date + " " + ex + " " + name + " " + mail;
    # текстовая часть сообщения (не забываем указать кодировку)
    msg.attach(MIMEText(mes_text, "plain", "utf-8"))
    # соединяемся с почтовым сервером и выполняем авторизацию
    server = SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login("gid.po.rimu", "bruihrhr843hr748hfre")
    # отправляем сформированное сообщение, после чего выходим
    server.sendmail(fromaddr, toaddr, msg.as_string())
    server.quit()
    return "OK"
    
