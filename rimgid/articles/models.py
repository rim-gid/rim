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
from decorators import PointedSaver
#from widgets import WithImageTextarea
#from fields import WithImageWysiwygField
        
@PointedSaver
class ArticleSpecial(models.Model):
    def dublicate_me_using(self,uss,**kwargs):
        kwargs['name'] = self.name
        kwargs['text'] = self.text
        kwargs['image'] = str(self.image)
        return self.dublicate_me_using_base(uss,**kwargs)
    def duplicate_objects_using(self,obj,uss,*args,**kwargs):
        pass
    def duplicate_files(self):
        print "image.path=", self.image.path
        self.git_add(self.image.path)
        self.git_push()
  
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
        self.fill_specials(ArticleTypeSpecial, obj, uss,*args,**kwargs)
    def duplicate_files(self):
        pass
  
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
    def duplicate_files(self):
        pass
            
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
    """
    Основной класс "статья". Наполнение сайта полностью определяется
    добавлением и редактированием статей. Остальные модели используются
    для их настройки.
    """
    def dublicate_me_using(self,uss,**kwargs):
        sites = []
        specials = []
        if 'sites' in kwargs:
            sites += kwargs['sites']
            del kwargs['sites']
        if 'specials' in kwargs:
            specials += kwargs['specials']
            del kwargs['specials']
        kwargs['url'] = self.url
        kwargs['title'] = self.title
        kwargs['atype'] = self.atype.duplicate_using(uss)
        me = self.dublicate_me_using_base(uss,**kwargs)
        kwargs['sites']=sites
        kwargs['specials']=specials
        #duplicate_objects_using(self, obj, uss, **kwargs)
        return me
    def duplicate_objects_using(self,obj,uss,*args,**kwargs):
        self.fill_sites(obj, uss, *args, **kwargs)
        self.fill_specials(ArticleSpecial, obj, uss, *args, **kwargs)
        obj.datetime = self.datetime
        obj.content = self.content
    def duplicate_files(self):
        pass
        
    #def save_m2m(self):
    #    print "----saving_m2m----"
    #    super(Article, self).save_m2m()
    
    """
    def save123(self):
        print "----saving----"
        #self.save(*args, **kwargs)
        super(Article, self).save()
        try:
            super(Article, self).save(using="pointed", force_insert=True)
        except:
            super(Article, self).save(using="pointed")
            print "PointedSaver ERROR"
    """

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
            if sp.image:
                return str(sp.image)
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
            
