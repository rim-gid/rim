# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from rimgid.wysiwyg import WYSIWYGField
import datetime
from django.contrib.sites.models import Site
from django.contrib.flatpages.models import FlatPage

class ArticleSpecial(models.Model):
    name = models.CharField(max_length = 200,blank = "True")
    text = WYSIWYGField(blank="True")
    
    stype = "article"
    
    def __unicode__(self):
        try:
            atype = self.article_set.all()[0].atype.title
        except:
            atype = ""
        return self.name + "["+atype+"] - " + self.text

class ArticleTypeSpecial(ArticleSpecial):
    stype = "articleType"

class ArticleType(models.Model):
    title = models.CharField(max_length=200)
    text = WYSIWYGField(null="True", blank="True")
   
    #url_prefix = models.CharField(max_length=200, blank="True")
    #url_prefix_needed = models.BooleanField(default=True)
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
            return sp.text
        except:
            return self.title

from rimgid.added.thumbs import ImageWithThumbsField

class Foto(models.Model):
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    text = WYSIWYGField(blank="True")
    #image = models.ImageField(upload_to="fotos/",null="True", blank="True")
    image = ImageWithThumbsField(upload_to='images', sizes=((200,200),))

    datetime = models.DateTimeField(blank="True")
    sites = models.ManyToManyField(Site)
    
    """
    def mini_img(self):
        #if self.image.width <= 200:
        #    return self.image
        aspect = self.image.height / self.image.width
        new_hei = 200*aspect
        new_sz = '200x'+str(new_hei)
        
        image_path = thumbnail(self.image, new_sz) # создается миниатюра
        
        #self.image.
        
        #image_path = image_path.replace('\\','/') # Windows-Fix
        #return '<a href="'+ str(self.id) +'/"><img src="'+ 
        #  str(image_path) +'"/></a>'
        return image_path
    """
    
    def __unicode__(self):
        return self.title + " - " + self.image.url_200x200

class Article(FlatPage):
    atype = models.ForeignKey(ArticleType)
    specials = models.ManyToManyField(ArticleSpecial, null="True", blank="True")
    datetime = models.DateTimeField(blank="True",default=datetime.datetime.now) #auto_now_add=True
    
    def special(self):#FIXME не нужна
        sp = self.specials.objects.values("name","text")
        print str(sp)
        return sp
        
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
    
    """
    def atype_url(self):
        try:
            self.atype.title
            sp = self.atype.specials.get(name='only_in_list')
        except:
            pass
        else:
            if sp.text == "True":
                return True
    """
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
        a = Article(title=ex.title, atype=ex_type, content=ex.text_full, url="/excursion/"+str(k))
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

def add_site_pole(a):
    site = Site.objects.get(id=settings.SITE_ID)
    a.sites.add(site)
    a.save()

def add_special(a,name,text):
    ar = get_article_special(name, text)
    a.specials.add(ar)
    a.save()
        
from views import file_text
        
from rimgid.articles.templatetags import articles_tags
        
# специальная функция для заполнения экскурсий
def fill_table(obj,type_name,trans_name,type_name_postfix="s",files=False):
    ex_type = get_article_type(type_name,True,False,trans_name)
    site = Site.objects.get(id=settings.SITE_ID)
    
    if len(type_name_postfix) > 0:
        print "adding atype postfix", ex_type.title, type_name_postfix
        ex_type.specials.add(get_article_type_special("type_name_postfix",type_name_postfix))
        ex_type.save()
    
    k = 1
    exs = obj.objects.order_by('id')
    for ex in exs:
        #print ex.title, ex.title_time, ex.text_full, ex.cost
        try:
            a = Article(title=ex.title, atype=ex_type, content=ex.text, url="/"+type_name+"_"+str(k))
        except:
            try:
                a = Article(title=ex.name, atype=ex_type, content=ex.text, url="/"+type_name+"_"+str(k))
            except:
                a = Article(title=ex.name, atype=ex_type, content=ex.value, url="/"+type_name+"_"+str(k))
        a.save()
        a.sites.add(site)
        a.save()
        k += 1
        
        try:
            mail = ex.mail
            add_special(a,"mail",mail)
        except:
            pass
        
        try:
            a.datetime = ex.date
            a.save()
        except:
            pass
        
        try:
            im = str(ex.image)
            if im == "0":
                continue
            if im[0] != '/':
                im = "/" + im
            add_special(a,"image",im)
        except:
            pass
    
    if files:
        for f in files:
            #global TEMP_ARTICLE_TITLE
            content = file_text(f)
            print "read_TEMP_ARTICLE_TITLE", articles_tags.TEMP_ARTICLE_TITLE
            title = articles_tags.TEMP_ARTICLE_TITLE
            a = Article(title=title, atype=ex_type, content=content, url="/"+type_name+"_"+str(k))
            a.save()
            a.sites.add(site)
            a.save()
            k += 1
            articles_tags.TEMP_ARTICLE_TITLE = ""
    
    ex_type = get_article_type("notes_page",False,"articles/notes.html",u"Список статей")
    #mp = get_main_params()
    #print ex.title, ex.title_time, ex.text_full, ex.cost
    a = Article(title=trans_name, atype=ex_type, content=type_name, url="/"+type_name + type_name_postfix) #type_name_postfix добавляет s в конце
    a.save()
    add_site_pole(a)
        
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
        
def fill_fotos():
  
    fotos = Fotos.objects.all()
    for f in fotos:
      
      #title = models.CharField(max_length=200)
      #text = WYSIWYGField()
      #upload_to=settings.MEDIA_ROOT+
      #image = models.ImageField(upload_to="images/",null="True")
      #date = models.DateField()
      im = str(f.image)
      try:
        if im[0] != '/':
          im = "/"+im
      except:
        pass
  
      foto = Foto(title=f.title, url="***", text=f.text, image=im, datetime=f.date)
      foto.save()
      add_site_pole(foto)
      #title = models.CharField(max_length=200)
      #url = models.CharField(max_length=200)
      #text = WYSIWYGField(blank="True")
      #image = models.ImageField(upload_to="fotos/",null="True", blank="True")
      #datetime = models.DateTimeField(blank="True")
      
    ex_type = get_article_type("fotogallery",False,"articles/fotos.html",u"Фотогалерея")
    a = Article(title=u"Фото", atype=ex_type, content="foto", url="/fotos")
    a.save()
    add_site_pole(a)

def fill_main_page():
    ex_type = get_article_type("simple_page",False,"articles/main.html",u"Заглавная страница")
    mp = get_main_params()
    
    #print ex.title, ex.title_time, ex.text_full, ex.cost
    a = Article(title=mp['owner_maintitle'], atype=ex_type, content=mp['owner_maintext'], url="/")
    a.save()
    add_site_pole(a)
    
def fill_yandex():
    ex_type = get_article_type("for_yandex",False,"articles/empty.html",u"Для Яндекса")
    mp = get_main_params()
    site = Site.objects.get(id=1)
  
    def add_simple_page(ext_type, mp, template, url, site):
        content = file_text(template)
        a = Article(title=mp['owner_maintitle'], atype=ex_type, content=content, url=url)
        a.save()
        a.sites.add(site)
        a.save()
      
    add_simple_page(ex_type, mp, "yandex_61b9f126eb948082.txt", "/yandex_61b9f126eb948082.txt", site)
    add_simple_page(ex_type, mp, "robots.txt", "/robots.txt", site)
    add_simple_page(ex_type, mp, "1be09f3f8a74.html", "/1be09f3f8a74.html", site)
  
    y_name = "yandex_metrika"
    y_value = file_text("articles/yandex_metrika")
    try:
        po = ProjectOption.objects.get(name=y_name, value=y_value)
    except:
        po = ProjectOption(name=y_name, value=y_value)
        po.save()
    else:
        pass
  
    try:
        po.sites.get(id=site)
    except:
        po.sites.add(site)
        po.save()
    print y_name, " - OK!"
    

def fill_translate():
    ex_type = get_article_type("translate",False,"articles/excursion.html",u"Услуги перевода")
    mp = get_main_params()
    
    datas = OlgaInfo.objects.all()
    data = datas[1].hello_text
    #db_template = Template(data.hello_text)
    #db_rez_template = Template('{% extends db_template %}')
    #db_c = Context(locals())
    #db_t = db_template.render(db_c)
    
    #print ex.title, ex.title_time, ex.text_full, ex.cost
    a = Article(title=u"Услуги перевода", atype=ex_type, content=data, url="/translate")
    a.save()
    add_site_pole(a)
    
filled = False

def fill_all():
    global filled
    
    if filled:
      return
    ProjectOption.objects.all().delete()
    ArticleSpecial.objects.all().delete()
    Article.objects.all().delete()
    ArticleType.objects.all().delete()
    Foto.objects.all().delete()
    
    fill_main_params()
    fill_excursions()
    fill_table(Note,"note",u"Новости")
    fill_table(Shops,"shop",u"Магазины")
    fill_table(Transport,"transport",u"Транспорт",type_name_postfix="")
    fill_table(Reccomendations,"reccomendation",u"Отзывы")
    fill_table(Flights,"flight",u"Авиаперелеты")
    fill_table(Hotels,"hotel",u"Отели")
    fill_table(Restaurants,"restaurant",u"Рестораны")
    fill_table(Contacts,"contact",u"Контакты")
    fill_table(Transfer,"transfer",u"Трансфер",type_name_postfix="",files=["articles/transfer_1","articles/transfer_2"])
    fill_main_page()
    fill_fotos()
    fill_yandex()
    fill_translate()
    
    filled = True

fill_all()



