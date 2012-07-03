# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from rimgid.wysiwyg import WYSIWYGField
import datetime
from django.contrib.sites.models import Site
from django.contrib.flatpages.models import FlatPage

#декоратор класса
def PointedSaver(cls):
    def save(self, *args, **kwargs):
        print "----saving----"
        super(cls,self).save(*args, **kwargs)
        duplicate_using(self,"pointed",*args,**kwargs)
    
    def dublicate_me_using_base(resource,uss,**kwargs):
        try:
            obj = cls.objects.using(uss).get(**kwargs)
        except:
            obj = cls(**kwargs)
            super(cls,obj).save(using=uss)
        return obj
        #return cls.objects.using(uss).get_or_create(using=uss,**kwargs)
    
    def duplicate_using(resource,uss,*args,**kwargs):
        obj = resource.dublicate_me_using(uss,**kwargs)
        resource.duplicate_objects_using(obj,uss,*args,**kwargs)
        super(cls,obj).save(using=uss)
        return obj
    
    #если нужно
    def fill_sites(self,obj, uss, *args, **kwargs):
        
        sites = self.sites.all()
        obj.sites.add(args)
        
        return
        for s in self.sites.all():
            try:
                new_s = Site.objects.using(uss).get(id=s.id)
            except:
                new_s = Site(name=s.name,domain=s.domain,id=s.id)
                #new_s.name = s.name
                #new_s.domain = s.domain
                #new_s.save(using=uss)
            #new_s, created = Site.objects.using(uss).get_or_create(id=s.id)
            #if created:
            #    new_s.name = s.name
            #    new_s.domain = s.domain
            
            #obj.sites.add(new_s)
            new_s.article_set.add(obj)
            new_s.save(using=uss)
        #super(cls,obj).save(using=uss)
    #если нужно
    def fill_specials(self,sp_type, obj, uss):
        for s in self.specials.all():
            new_s, created = sp_type.objects.using(uss).get_or_create(name=s.name,text=s.text)
            obj.specials.add(new_s)
        
    cls.save = save
    cls.duplicate_using = duplicate_using
    cls.fill_sites = fill_sites
    cls.fill_specials = fill_specials
    cls.dublicate_me_using_base = dublicate_me_using_base
    return cls
        
@PointedSaver
class ArticleSpecial(models.Model):
    def dublicate_me_using(self,uss,**kwargs):
        kwargs['name'] = self.name
        kwargs['text'] = self.text
        return self.dublicate_me_using_base(uss,**kwargs)
    def duplicate_objects_using(self,obj,uss,*args,**kwargs):
        pass
  
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

@PointedSaver
class ArticleType(models.Model):
    def dublicate_me_using(self,uss,**kwargs):
        kwargs['title'] = self.title
        kwargs['text'] = self.text
        return self.dublicate_me_using_base(uss,**kwargs)
    #def duplicate_params(self):
    #    kwargs = {}
    #    kwargs['title'] = self.title
    #    kwargs['text'] = self.text
    #    return kwargs
    def duplicate_objects_using(self, obj, uss,*args,**kwargs):
        self.fill_specials(ArticleTypeSpecial, obj, uss)
  
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
   
"""
def update_sites(sender, instance, created, **kwargs):
    if created and instance.status == 1:
        title = instance.title.encode('utf-8') # у меня на одном из проектов ругался на кодировку
        for item in Subscrib.objects.all():
            to_email = item.email
            subject = 'Новая новость на сайте'
            html_content = '<p><i>Здравствуйте</i></p>'
            html_content += 'Новая новость: <a href="http://developtolive.com/news/%s/">%s</a>' % (instance.id, title)
            html_content +='<p><i>Отписаться от рассылки можно по <a href="http://developtolive.com/send/sub/no/?email=%s">ссылке</a></i></p>' % (item.id)
            html_content += '<p><i>Всего доброго.</i></p>'
            from_email = 'i@developtolive.com'
            msg = EmailMessage(subject, html_content, from_email, [to_email])
            msg.content_subtype = "html"
            msg.send()
            
signals.post_save.connect(go_subscrib, sender=News)
"""

from rimgid.added.thumbs import ImageWithThumbsField

@PointedSaver
class Foto(models.Model):
    def dublicate_me_using(self,uss,**kwargs):
        kwargs['url'] = self.url
        kwargs['title'] = self.title
        kwargs['text'] = self.text
        kwargs['image'] = self.image
        return self.dublicate_me_using_base(uss,**kwargs)
    def duplicate_objects_using(self, obj, uss,*args,**kwargs):
        self.fill_sites(obj, uss)
            
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    text = WYSIWYGField(blank="True")
    image = ImageWithThumbsField(upload_to='images', sizes=((200,200),))    #image = models.ImageField(upload_to="fotos/",null="True", blank="True")

    datetime = models.DateTimeField(blank="True")
    sites = models.ManyToManyField(Site)

    def __unicode__(self):
        return self.title + " - " + self.image.url_200x200

@PointedSaver
class Article(FlatPage):
    def dublicate_me_using(self,uss,**kwargs):
        kwargs['url'] = self.url
        kwargs['title'] = self.title
        kwargs['atype'] = self.atype.duplicate_using(uss)
        return self.dublicate_me_using_base(uss,**kwargs)
    def duplicate_objects_using(self,obj,uss,*args,**kwargs):
        #at, at_created = ArticleType.objects.using(uss).get_or_create(title=self.atype.title,text=self.atype.text)
        #obj.atype = self.atype.duplicate_using(uss)
        self.fill_sites(obj, uss, *args, **kwargs)
        self.fill_specials(ArticleSpecial, obj, uss, **kwargs)
        obj.datetime = self.datetime
        obj.content = self.content

    def save123(self):
        print "----saving----"
        #self.save(*args, **kwargs)
        super(Article, self).save()
        try:
            super(Article, self).save(using="pointed", force_insert=True)
        except:
            super(Article, self).save(using="pointed")
            print "PointedSaver ERROR"






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
            
# *************************************************************
#  Далее функционал для перегона таблиц из старой версии в новую
# *************************************************************
"""
from rimgid.books.models import *
from django.contrib.sites.models import Site
from views import file_text
        
from rimgid.articles.templatetags import articles_tags
        
from settings import get_main_params
from rimgid.templatetags.models import ProjectOption

#from project_params_2 import AAA_SITE_PARAMS as mp2

site_repaired = False

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

def get_site(site_id=settings.SITE_ID):
    global site_repaired
    if not site_repaired:
        print "Sites repairing..."
        sts = ['rim-gid.com','gidinrome.com']
        #sites = Site.objects.all()#.delete()
        k = 1
        for s in sts:
            def get_save_using(s, k, uss):
                try:
                    si = Site.objects.using(uss).get(id=k)
                except:
                    si = Site(name=s,domain=s,id=k)
                    print "new site ", s, ' site_id=', k
                si.name = s
                si.domain = s
                try:
                    si.save(using=uss, force_insert=True)
                except:
                    print uss, " allready contains id=", k
            get_save_using(s, k, "default")
            get_save_using(s, k, "pointed")
            k += 1
        site_repaired = True
  
    return Site.objects.get(id=site_id)
    
def add_site_pole(a, site_id=settings.SITE_ID):
    site = Site.objects.get(id=site_id)
    a.sites.add(site)
    a.save()

def add_special(a,name,text):
    ar = get_article_special(name, text)
    a.specials.add(ar)
    a.save()
        
def add_site_to(obj,site_id=settings.SITE_ID):
    try:
        obj.sites.get(id=site_id)
    except:
        obj.sites.add(get_site(site_id))
        obj.save()
        
def add_option(name, value, site_id=settings.SITE_ID):
    #try:
    #    value = str(value)
    #except:
    #    print "option FALSE! ", name
    try:
        po = ProjectOption.objects.get(name=value, value=value)
        add_site_to(po, site_id)
    except:
        try:
            po = ProjectOption(name=name, value=value)
            po.save()
            add_site_to(po, site_id)
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
def fill_excursions():
    ex_type = get_article_type("excursion",False,"articles/excursion.html",u"Экскурсии|Excursions")#ArticleType.objects.get(title="Excursion")
    def add_ex(site_id=1,uss="rus"):
        print "fill excursions ", uss
        site = Site.objects.get(id=site_id)
        k = 1
        exs = Excursion.objects.using(uss).order_by('id')
        for ex in exs:
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
    add_ex(1,"rus")
    add_ex(2,"eng")
        
# специальная функция для заполнения экскурсий
def fill_table(obj,type_name,trans_name,type_name_postfix="s",files=False,massive=False,site_id=settings.SITE_ID,only_in_list=True,create_list_page=True,uss=False):
    ex_type = get_article_type(type_name,only_in_list,False,trans_name)
    site = Site.objects.get(id=site_id)
    
    try:
        trans_name = trans_name.split("|")[site_id-1]
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
        if uss:
            exs = obj.objects.using(uss).order_by('id')
        else:
            exs = obj.objects.order_by('id')
        for ex in exs:
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
        get_article(title=trans_name, atype=ex_type, content=type_name, url="/"+type_name + type_name_postfix, site_id=site_id)
        
def fill_main_params():
    def add_ops(mp, k):
        for m in mp:
            if m == "local":
                continue
            add_option(m, mp[m], k)
            print m, k, mp[m]
    add_ops(get_main_params(), 2)
    add_ops(mp2, 1)
    my_vk = [u"Моя страница вконтакте","my page in vk.com"]
    k = 1
    for m in my_vk:
        add_option("my_vkontakte_page", m, k)
        k += 1
    
#********************************ok
        
def fill_fotos(uss=False, site_id=settings.SITE_ID):
    if uss:
        fotos = Fotos.objects.using(uss).all()
    else:
        fotos = Fotos.objects.all()
    for f in fotos:
        im = str(f.image)
        try:
            if im[0] != '/':
                im = "/"+im
        except:
            pass  
        foto = Foto(title=f.title, url="***", text=f.text, image=im, datetime=f.date)
        foto.save()
        add_site_pole(foto, site_id)      
    ex_type = get_article_type("fotogallery",False,"articles/fotos.html",u"Фотогалерея|Photogallery")
    fts = [u"Фото","Photo"]
    a = Article(title=fts[site_id-1], atype=ex_type, content="foto", url="/fotos")
    a.save()
    add_site_pole(a, site_id)

def fill_main_page(mmp, site_id=settings.SITE_ID):
    ex_type = get_article_type("main_page",False,"articles/main.html",u"Заглавная страница|Main page")
    a = Article(title=mmp['owner_maintitle'], atype=ex_type, content=mmp['owner_maintext'], url="/")
    a.save()
    add_site_pole(a, site_id)
    
def fill_yandex():
    ex_type = get_article_type("for_yandex",False,"articles/empty.html",u"Для Яндекса")
    mp = mp2
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

def fill_translate(uss=False, site_id=settings.SITE_ID):
    ex_type = get_article_type("translate",False,"articles/excursion.html",u"Услуги перевода|Translations")
    mp = get_main_params()
    datas = OlgaInfo.objects.using(uss).all()
    data = datas[1].hello_text
    trs = [u"Услуги перевода","Translations"]
    a = get_article(title=trs[site_id-1], atype=ex_type, content=data, url="/translate", site_id=site_id)

filled = False

def fill_transfer():
    ex_type = get_article_type("simple_page",False,"articles/simple_page.html",u"Простая страница|Simple page")
    files = ["articles/transfer_1_ru","articles/transfer_1_eng"]
    fill_articles_from_files_sitable(ex_type, files, "/transfer")
    
def fill_friends():
    m_ru = [ ["http://www.florenceguide.ru/","tatiana_matushko.jpg",u"Татьяна Матюшко - Экскурсии по Флоренции"],
      ["http://www.russianflorence.com/","tatiana_usova.jpg",u"Татьяна Усова - Экскурсии по Флоренции"],
      ["http://www.guidaavenezia.com/ru/contatti_ru.htm","guida_turistica.jpg","Гид в Венеции"],
      ["http://www.interhome.ru","interhome.jpg",u"Туристическая компания"], ]
    m_eng = [ ["http://www.interhome.ru","interhome.jpg",u"Tourist company"], ]
    fill_table(False,"friend",u"Друзья|Friends",type_name_postfix="s",site_id=1, massive=m_ru,create_list_page=False)
    fill_table(False,"friend",u"Друзья|Friends",type_name_postfix="s",site_id=2, massive=m_eng,create_list_page=False)

def fill_tables(uss, site_id):
    fill_fotos(uss, site_id)
    fill_translate(uss, site_id)
  
    fill_table(Note,"note",u"Новости|Notes",uss=uss,site_id=site_id)
    fill_table(Shops,"shop",u"Магазины|Shops",uss=uss,site_id=site_id)
    fill_table(Transport,"transport",u"Транспорт|Transport",type_name_postfix="",uss=uss,site_id=site_id)
    fill_table(Reccomendations,"reccomendation",u"Отзывы|Reccomendations",uss=uss,site_id=site_id)
    fill_table(Flights,"flight",u"Авиаперелеты|Flights",uss=uss,site_id=site_id)
    fill_table(Hotels,"hotel",u"Отели|Hotels",uss=uss,site_id=site_id)
    fill_table(Restaurants,"restaurant",u"Рестораны|Restaurants",uss=uss,site_id=site_id)
    fill_table(Contacts,"contact",u"Контакты|Contacts",uss=uss,site_id=site_id)
    #fill_table(Transfer,"transfer",u"Трансфер",type_name_postfix="",files=["articles/transfer_1","articles/transfer_2"])
    fill_table(False,"italy",u"Другие города Италии|Other Italy cities",type_name_postfix="",uss=uss,site_id=site_id)

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
    
    fill_main_page(get_main_params(), 2)
    fill_main_page(mp2, 1)
    
    fill_yandex()
    fill_transfer()
    fill_friends()
    
    fill_tables("rus",1)
    fill_tables("eng",2)
    
    filled = True
"""
#get_site()
#fill_all()
#ProjectOption.objects.all().delete()
#fill_main_params()

print "SITE_ID = ", settings.SITE_ID


def ttt():
    aa = Article.objects.using("pointed").all()
    for a in aa:
      print a.title

#ttt()


import pickle
def save_articles():
    wf = open("wf.bsql","w")
    aa = Article.objects.all()
    for a in aa:
        pickle.dump(a, wf)
    wf.close()
    
def load_articles():
    f = open("wf.bsql")
    
    def sites_nums(a):
        li = []
        for asi in a.sites.all():
            print "id ", asi.id
            li += [asi.id]
        return li
    
    def peresec(li1, li2):
        for li in li1:
            for lia in li2:
                if lia == li:
                    return True
        return False
    
    def find_same(ar, ar_li):
        finded = False
        aa = Article.objects.filter(url=ar.url) #using("pointed").
        for a in aa:
            a_li = sites_nums(a)
            #a_all = str(a.sites.all())
            if peresec(a_li, ar_li):
                #print "   ", a_li
                finded = True
                break
        return finded
    
    while True:
        try:
            ar = pickle.load(f)
            #ar_all = str(ar.sites.all())
            ar_li = sites_nums(ar)
            #print "loaded ", ar_li
        except:
            break

        if find_same(ar, ar_li):
            print "url = ", ar.url, " ", ar_li, " FINDED!!! "
        else:
            print "url = ", ar.url, " ", ar_li, " NOT finded!!!"
          
    #a = Article.objects.all()[0]
    #pickle.dump(a, wf)
    f.close()

