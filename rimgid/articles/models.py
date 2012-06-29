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
            try:
                sps = sp.text.split("|")
                return sps[settings.SITE_ID-1]
            except:
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
            
# *************************************************************
#  Далее функционал для перегона таблиц из старой версии в новую
# *************************************************************
            
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

site_repaired = False

def get_site(site_id=settings.SITE_ID):
    global site_repaired
    if not site_repaired:
        print "Sites repairing..."
        sts = ['rim-gid.com','gidinrome.com']
        sites = Site.objects.all().delete()
        k = 1
        for s in sts:
            si = Site(name=s,domain=s,id=k)
            si.save()
            print si.name, ' site_id=', si.id    
            k += 1
        site_repaired = True
  
    return Site.objects.get(id=site_id)
    
#get_site()

# специальная функция для заполнения экскурсий
def fill_excursions():
    ex_type = get_article_type("excursion",False,"articles/excursion.html",u"Экскурсии|Excursions")#ArticleType.objects.get(title="Excursion")
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
        
from settings import get_main_params
from rimgid.templatetags.models import ProjectOption
        
def add_site_to(obj,site_id=settings.SITE_ID):
    try:
        obj.sites.get(id=site_id)
    except:
        obj.sites.add(get_site(site_id))
        obj.save()
        
def add_option(name,value,site_id=settings.SITE_ID):
    try:
        value = str(value)
    except:
        print "option FALSE! ", name
    try:
        po = ProjectOption.objects.get(name=value, value=value)
    except:
	try:
            po = ProjectOption(name=name, value=value)
            po.save()
            add_site_to(po,site_id)
        except:
            print "option ERROR! ", name

def get_article(title,atype,content,url,site_id=settings.SITE_ID):
    try:
        a = Article.objects.get(title=title, atype=atype, content=content, url=url)
    except:
        a = Article(title=title, atype=atype, content=content, url=url)
        a.save()
        add_site_to(a,site_id)
    return a
        
# специальная функция для заполнения экскурсий
def fill_table(obj,type_name,trans_name,type_name_postfix="s",files=False,massive=False,site_id=settings.SITE_ID,only_in_list=True,create_list_page=True):
    ex_type = get_article_type(type_name,only_in_list,False,trans_name)
    site = Site.objects.get(id=site_id)
    
    try:
        trans_name = trans_name.split("|")[settings.SITE_ID-1]
    except:
        pass
    
    if len(type_name_postfix) > 0:
        print "adding atype postfix", ex_type.title, type_name_postfix
        ex_type.specials.add(get_article_type_special("type_name_postfix",type_name_postfix))
        ex_type.save()
    
    def add_image_special(a,img):#ex.image
        try:
            im = str(img)
            if im == "0":
                return
            if im[0] != '/':
                im = "/" + im
            add_special(a,"image",im)
        except:
            pass
    
    k = 1
    if obj:
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
            
            add_image_special(a,ex.image)
        
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
            
    #[ ["http://www.interhome.ru","/interhome.jpg",u"Tourist company"] ]
    if massive:
        for ma in massive:
            content = ma[2]
            title = ma[2]
            a = Article(title=title, atype=ex_type, content=content, url=ma[0])
            a.save()
            a.sites.add(site)
            sp = get_article_special("button_image", ma[1])
            a.specials.add(sp)
            a.save()
            k += 1
            
    if create_list_page:
        ex_type = get_article_type("notes_page",False,"articles/notes.html",u"Список статей|List of pages")
        #mp = get_main_params()
        #print ex.title, ex.title_time, ex.text_full, ex.cost
        #a = Article(title=trans_name, atype=ex_type, content=type_name, url="/"+type_name + type_name_postfix) #type_name_postfix добавляет s в конце
        #a.save()
        #add_site_pole(a)
        get_article(title=trans_name, atype=ex_type, content=type_name, url="/"+type_name + type_name_postfix, site_id=settings.SITE_ID)
        

        
def fill_main_params():
    site = Site.objects.get(id=settings.SITE_ID)
  
    mp = get_main_params()
    for m in mp:
        if m == "local":
            continue
        add_option(m,mp[m])
        print m, mp[m]
        
    my_vk = [u"Моя страница вконтакте","my page in vk.com"]
    k = 1
    for m in my_vk:
        add_option("my_vkontakte_page",m,k)
        k += 1
    
        
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
      
    ex_type = get_article_type("fotogallery",False,"articles/fotos.html",u"Фотогалерея|Photogallery")
    fts = [u"Фото","Photo"]
    a = Article(title=fts[settings.SITE_ID-1], atype=ex_type, content="foto", url="/fotos")
    a.save()
    add_site_pole(a)

def fill_main_page():
    ex_type = get_article_type("main_page",False,"articles/main.html",u"Заглавная страница|Main page")
    mp = get_main_params()
    
    #print ex.title, ex.title_time, ex.text_full, ex.cost
    a = Article(title=mp['owner_maintitle'], atype=ex_type, content=mp['owner_maintext'], url="/")
    a.save()
    add_site_pole(a)
    
def fill_yandex():
    ex_type = get_article_type("for_yandex",False,"articles/empty.html",u"Для Яндекса")
    mp = get_main_params()
    site = Site.objects.get(id=1)
  
    def add_empty_page(ext_type, mp, template, url, site):
        content = file_text(template)
        a = Article(title=mp['owner_maintitle'], atype=ex_type, content=content, url=url)
        a.save()
        a.sites.add(site)
        a.save()
      
    add_empty_page(ex_type, mp, "yandex_61b9f126eb948082.txt", "/yandex_61b9f126eb948082.txt", site)
    add_empty_page(ex_type, mp, "robots.txt", "/robots.txt", site)
    add_empty_page(ex_type, mp, "1be09f3f8a74.html", "/1be09f3f8a74.html", site)
  
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
   
"""
def add_simple_page(ex_type, template, url, site_id=settings.SITE_ID):
    content = file_text(template)
    print "read_TEMP_ARTICLE_TITLE", articles_tags.TEMP_ARTICLE_TITLE
    title = articles_tags.TEMP_ARTICLE_TITLE
    a = get_article(title=title, atype=ex_type, content=content, url=url, site_id=site_id)    
    articles_tags.TEMP_ARTICLE_TITLE = ""
"""

def get_article_from_file(ex_type, file_, url, site_id=settings.SITE_ID):
    content = file_text(file_)
    print "read_TEMP_ARTICLE_TITLE", articles_tags.TEMP_ARTICLE_TITLE
    title = articles_tags.TEMP_ARTICLE_TITLE
    a = get_article(title=title, atype=ex_type, content=content, url=url, site_id=site_id)    
    articles_tags.TEMP_ARTICLE_TITLE = ""
    return a

def fill_articles_from_files_sitable(ex_type, files, url):
    k = 1
    for f in files:
        get_article_from_file(ex_type, f, url, k)
        k += 1

"""
def add_simple_pages(ex_type, mp, template, url, site_id=settings.SITE_ID)
    k = 1
    for tr in trs:
        add_simple_page(ext_type, template, url, site)
        #get_article(title=tr, atype=ex_type, content=data, url="/translate",site_id=k)
        k += 1
"""

def fill_translate():
    ex_type = get_article_type("translate",False,"articles/excursion.html",u"Услуги перевода|Translations")
    mp = get_main_params()
    
    datas = OlgaInfo.objects.all()
    data = datas[1].hello_text
    trs = [u"Услуги перевода","Translations"]
    site_id = settings.SITE_ID
    a = get_article(title=trs[site_id-1], atype=ex_type, content=data, url="/translate", site_id=site_id)

filled = False

def fill_transfer():
    ex_type = get_article_type("simple_page",False,"articles/simple_page.html",u"Простая страница|Simple page")
    mp = get_main_params()
    site = get_site()
      
    files = ["articles/transfer_1_ru","articles/transfer_1_eng"]
    fill_articles_from_files_sitable(ex_type, files, "/transfer")
    #add_simple_pages(ex_type, files[site.id-1], "/transfer", site)
    
def fill_friends():
    m_ru = [ ["http://www.florenceguide.ru/","tatiana_matushko.jpg",u"Татьяна Матюшко - Экскурсии по Флоренции"],
      ["http://www.russianflorence.com/","tatiana_usova.jpg",u"Татьяна Усова - Экскурсии по Флоренции"],
      ["http://www.guidaavenezia.com/ru/contatti_ru.htm","guida_turistica.jpg","Гид в Венеции"],
      ["http://www.interhome.ru","interhome.jpg",u"Туристическая компания"], ]
    m_eng = [ ["http://www.interhome.ru","interhome.jpg",u"Tourist company"], ]
    fill_table(False,"friend",u"Друзья|Friends",type_name_postfix="s",site_id=1, massive=m_ru,create_list_page=False)
    fill_table(False,"friend",u"Друзья|Friends",type_name_postfix="s",site_id=2, massive=m_eng,create_list_page=False)

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
    fill_table(Note,"note",u"Новости|Notes")
    fill_table(Shops,"shop",u"Магазины|Shops")
    fill_table(Transport,"transport",u"Транспорт|Transport",type_name_postfix="")
    fill_table(Reccomendations,"reccomendation",u"Отзывы|Reccomendations")
    fill_table(Flights,"flight",u"Авиаперелеты|Flights")
    fill_table(Hotels,"hotel",u"Отели|Hotels")
    fill_table(Restaurants,"restaurant",u"Рестораны|Restaurants")
    fill_table(Contacts,"contact",u"Контакты|Contacts")
    #fill_table(Transfer,"transfer",u"Трансфер",type_name_postfix="",files=["articles/transfer_1","articles/transfer_2"])
    fill_main_page()
    fill_fotos()
    fill_yandex()
    fill_translate()
    fill_transfer()
    fill_table(False,"italy",u"Другие города Италии|Other Italy cities",type_name_postfix="")
    fill_friends()
    
    filled = True

#get_site()
#fill_all()



