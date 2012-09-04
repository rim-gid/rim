# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from rimgid.wysiwyg import WYSIWYGField
import datetime
from django.contrib.sites.models import Site
from django.contrib.flatpages.models import FlatPage
from django.utils.text import truncate_words
from django.utils.html import strip_tags
from rimgid.added.thumbs import ImageWithThumbsField
from django.db.models.signals import post_save
from rimcelery import tasks

def add_image_to_tasks(path):
    """
    Добавляет задание на копирование файла
    """
    tasks.duplicate_image.apply_async( [path] )
    print "TASK ADDED..."
        
class ArticleSpecial(models.Model):
    """
    Модель "Особенности статьи" - используется в модели Article
    """
    name = models.CharField(max_length = 200, blank = "True")
    text = WYSIWYGField(blank="True")
    image = models.ImageField(default=False, upload_to='images', null="True")
    
    stype = "article"

    def __unicode__(self):
        try:
            atype = self.article_set.all()[0].atype.title
        except:
            atype = ""
        txt = strip_tags(self.text)
        txt = self.name + " ["+atype+"] = " + txt
        k = 50
        if len(txt) > k:
            txt = txt[:k-3] + "..."
        if self.image:
            txt += " img:" + str(self.image)
        return txt
        
# Добавляем задание на копирование файла из ArticleSpecial
def special_save_handler(sender, **kwargs):
    print "special_save_handler", kwargs['instance'].image
    add_image_to_tasks(str(kwargs['instance'].image))
    
# После сохранения ArticleSpecial будет выполнена special_save_handler
post_save.connect(special_save_handler, sender=ArticleSpecial)

class ArticleTypeSpecial(ArticleSpecial):
    """
    Модель "Особенности типа статьи" - используется в модели ArticleType
    """
    stype = "articleType"

class ArticleType(models.Model):
    """
    Модель "Тип статьи" - используется для определения способа вывода статьи и задания общих особенностей
    """
    title = models.CharField(max_length=200)
    text = WYSIWYGField(null="True", blank="True")
   
    def type_name_postfix(self):
        try:
            sp = self.specials.get(name="type_name_postfix")
            return sp.text
        except:
            return ""
            
    def title_with_postfix(self):
        return self.title + self.type_name_postfix()
    
    specials = models.ManyToManyField(ArticleTypeSpecial, null="True", blank="True")
    
    def __unicode__(self):
        try:
            sp = self.specials.get(name="name")
            try:
                sps = sp.text.split("|")
                return sps[settings.SITE_ID-1]
            except:
                return sp.text
        except:
            return self.title
   
class Foto(models.Model):
    """
    Модель "Фото" - используется в галерее фотографий (страница фото)
    """
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    text = WYSIWYGField(blank="True")
    image = ImageWithThumbsField(upload_to='images', sizes=((200,200),))    #image = models.ImageField(upload_to="fotos/",null="True", blank="True")

    datetime = models.DateTimeField(blank="True")
    sites = models.ManyToManyField(Site)

    def __unicode__(self):
        return self.title + " - " + self.image.url_200x200
        
# добавляем задание на копирование двух файлов из Foto
def foto_save_handler(sender, **kwargs):
    print "foto_save_handler"
    print kwargs['instance'].image, kwargs['instance'].image.url_200x200
    add_image_to_tasks(kwargs['instance'].image)
    add_image_to_tasks(kwargs['instance'].image.url_200x200)
    
# После сохранения Foto будет выполнена foto_save_handler
post_save.connect(foto_save_handler, sender=Foto)

class Article(FlatPage):
    """
    Основной класс "статья". Наполнение сайта полностью определяется
    добавлением и редактированием статей. Остальные модели используются
    для их настройки.
    """
    atype = models.ForeignKey(ArticleType)
    specials = models.ManyToManyField(ArticleSpecial, null="True", blank="True")
    datetime = models.DateTimeField(blank="True",default=datetime.datetime.now) #auto_now_add=True
        
    # узнаем заданную особенность 'image'
    def image(self):
        try:
            sp = self.specials.get(name='image')
            if sp.image:
                return str(sp.image)
            return sp.text
        except:
            return False
    
    # проверяем, что не нужно создавать свою страницу
    def is_only_in_list(self):
        try:
            sp = self.atype.specials.get(name='only_in_list')
        except:
            pass
        else:
            if sp.text == "True":
                return True
        return False
    
    def __init__(self, *args, **kwargs):
        """
        Берем особенности из выбранного типа статьи
        """
        super(Article, self).__init__( *args, **kwargs)
        if len(self.template_name)>0:
            return
        try:
            a_t = self.atype.specials.get(name='article_template')
        except:
            pass
        else:
            self.template_name = a_t.text
        try:
            a_t = self.atype.specials.get(name='article_title')
        except:
            pass
        else:
            self.title = a_t.text
            
