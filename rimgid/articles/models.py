# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from rimgid.wysiwyg import WYSIWYGField
from django.contrib.flatpages.models import FlatPage
import datetime

class ArticleSpecial(models.Model):
    name = models.CharField(max_length = 200,blank = "True")
    text = WYSIWYGField(blank="True")
    
    stype = "article"
    
    def __unicode__(self):
        return self.name + " - " + self.text

class ArticleTypeSpecial(ArticleSpecial):
    stype = "articleType"

class ArticleType(models.Model):
    title = models.CharField(max_length=200)
    text = WYSIWYGField(null="True", blank="True")
   
    #url_prefix = models.CharField(max_length=200, blank="True")
    #url_prefix_needed = models.BooleanField(default=True)
    
    specials = models.ManyToManyField(ArticleTypeSpecial, null="True", blank="True")
    
    def __unicode__(self):
        try:
            sp = self.specials.get(name="name")
            return sp.text
        except:
            return self.title

class Foto(models.Model):
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    text = WYSIWYGField(blank="True")
    image = models.ImageField(upload_to="fotos/",null="True", blank="True")
    datetime = models.DateTimeField(blank="True")
    
    def __unicode__(self):
        return self.title

class Article(FlatPage):
    atype = models.ForeignKey(ArticleType)
    specials = models.ManyToManyField(ArticleSpecial, null="True", blank="True")
    datetime = models.DateTimeField(blank="True",default=datetime.datetime.now) #auto_now_add=True
    
    def special(self):
        #print "special", self.name
        sp = self.specials.objects.values("name","text")
        print str(sp)
        return sp
        #return "----"
        #try:
        #    return sp.text
        #except:
        #    return False
        
    def image(self):
        try:
            sp = self.specials.get(name='image')
            return sp.text
        except:
            return False
    
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
        super(FlatPage, self).__init__( *args, **kwargs)
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
            
from rimgid.books.models import *
from django.contrib.sites.models import Site

def get_article_special(name, text):
    try:
        a = ArticleSpecial.objects.get(name=name,text=text)
    except:
        a = ArticleSpecial(name=name,text=text)
        a.save()
    return a

def get_article_type_special(name, text):
    try:
        a = ArticleTypeSpecial.objects.get(name=name,text=text)
    except:
        a = ArticleTypeSpecial(name=name,text=text)
        a.save()
    return a

def get_article_type(name,only_li=True,ar_t_template=False,type_name=False):
    try:
        a = ArticleType.objects.get(title=name)
    except:
        a = ArticleType(title=name)
        a.save()
        if only_li:
            a.specials.add(get_article_type_special("only_in_list","True"))
        if ar_t_template:
            a.specials.add(get_article_type_special("article_template",ar_t_template))
        if type_name:
            a.specials.add(get_article_type_special("name",type_name))
        a.save()
    return a

# специальная функция для заполнения экскурсий
def fill_excursions():
    ex_type = get_article_type("excursion",False,"articles/excursion.html","Экскурсии")#ArticleType.objects.get(title="Excursion")
    site = Site.objects.get(id=settings.SITE_ID)
    
    #ArticleSpecial(name="small_text",text=ex.text)
    k = 1
    
    exs = Excursion.objects.order_by('id')
    for ex in exs:
        #print ex.title, ex.title_time, ex.text_full, ex.cost
        a = Article(title=ex.title, atype=ex_type, content=ex.text_full, url="/excursion_"+str(k)+"/")
        a.save()
        a.sites.add(site)
        
        if ex.title_time != "0":
            sp = get_article_special("excursion_time", ex.title_time)
            a.specials.add(sp)
        if ex.cost != "0":
            sp = get_article_special("cost", ex.cost)
            a.specials.add(sp)
        if ex.button_image != "0":
            sp = get_article_special("button_image", ex.button_image)
            a.specials.add(sp)
        if ex.map_address != "0":
            sp = get_article_special("map_address", ex.map_address)
            a.specials.add(sp)
        
        a.save()
        
        k += 1



        
# специальная функция для заполнения экскурсий
def fill_table(obj,type_name,trans_name):
    ex_type = get_article_type(type_name,True,False,trans_name)
    site = Site.objects.get(id=settings.SITE_ID)
    
    k = 1
    exs = obj.objects.order_by('id')
    for ex in exs:
        #print ex.title, ex.title_time, ex.text_full, ex.cost
        a = Article(title=ex.title, atype=ex_type, content=ex.text, url="/"+type_name+"_"+str(k)+"/")
        a.save()
        a.sites.add(site)
        a.save()
        k += 1
        
        try:
            a.datetime = ex.date
            a.save()
        except:
            pass
        
        try:
            im = ex.image.url()
            ar = get_article_special("image", im)
            a.specials.add(ar)
            a.save()
        except:
            try:
                im = ex.image
                
                if im == "0":
                    continue
                if im[0] != '/':
                    im = "/" + im
                ar = get_article_special("image", im)
                a.specials.add(ar)
                a.save()
            except:
                pass
    
    ex_type = get_article_type("notes_page",False,"articles/notes.html",u"Список статей")
    mp = get_main_params()
    
    #print ex.title, ex.title_time, ex.text_full, ex.cost
    a = Article(title=trans_name, atype=ex_type, content=type_name, url="/"+type_name+"s/")
    a.save()
    a.sites.add(site)
    a.save()
        
from settings import get_main_params
from rimgid.templatetags.models import ProjectOption
        
def fill_main_params():
    site = Site.objects.get(id=settings.SITE_ID)
  
    mp = get_main_params()
    for m in mp:
        if m == "local":
            continue
        try:
            po = ProjectOption.objects.get(name=m, value=mp[m])
        except:
            po = ProjectOption(name=m, value=mp[m])
            po.save()
        else:
            pass
      
        try:
            po.sites.get(id=settings.SITE_ID)
        except:
            po.sites.add(site)
            po.save()
        print m, mp[m]

def fill_main_page():
    site = Site.objects.get(id=settings.SITE_ID)
    
    ex_type = get_article_type("simple_page",False,"articles/main.html",u"Простая страница")
    mp = get_main_params()
    
    #print ex.title, ex.title_time, ex.text_full, ex.cost
    a = Article(title=mp['owner_maintitle'], atype=ex_type, content=mp['owner_maintext'], url="/main/")
    a.save()
    a.sites.add(site)
    a.save()

def fill_all():
    ArticleSpecial.objects.all().delete()
    Article.objects.all().delete()
    ArticleType.objects.all().delete()
    fill_excursions()
    fill_table(Note,"note",u"Новости")
    fill_table(Shops,"shop",u"Магазины")
    fill_table(Transport,"transport",u"Транспорт")
    fill_main_page()
    #fill_main_params()

fill_all()