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

def excursion_order(request,ex,mail,text):
    """
    запрос отправки заказа
    """
    rez = accounts_profile(request,ex,mail,text);
    return HttpResponse(str(rez), mimetype="text/html")

def contact_form(request,ex=""):
    if request.method == 'POST':
        mp = get_main_params()
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
              return HttpResponse(mp['msg_thx'], mimetype="text/html");
            er_str = mp['msg_error'];
            er_str += mp['msg_error_repeat'];
            er_str += mp['msg_error_contacts'];
            return HttpResponse(er_str, mimetype="text/html");
    else:
        form = ContactForm(
            #initial={'subject': 'I love your site!'}
        )
    return render_to_response('contact_form.html', locals())

def accounts_profile(request,name,ex,mail,text,date):
    """
    отправка заказа
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
      mes_text += "\n---server version: "+settings.AAA_SITE_PARAMS.site_version
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
    
"""
    FIXME to check and delete From giginrome.com
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
    server.login("gid.po.rimu", "bruihrhr843hr748hfre")
    # отправляем сформированное сообщение, после чего выходим
    server.sendmail(fromaddr, toaddr, msg.as_string())
    server.quit()
    #os.system("/home/git/test")
    return "OK"
    
"""