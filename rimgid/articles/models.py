# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from rimgid.wysiwyg import WYSIWYGField
from django.contrib.flatpages.models import FlatPage
import datetime

class ArticleSpecial(models.Model):
    # префикс url. 
    name = models.CharField(
      max_length = 200,
      blank = "True"
    )
    text = WYSIWYGField(
      blank="True"
    )
    
    stype = "article"
    
    def __unicode__(self):
        return self.name + " - " + self.text

class ArticleTypeSpecial(ArticleSpecial):
    stype = "articleType"

class ProjectSpecial(ArticleSpecial):
    stype = "articleType"

class ArticleType(models.Model):
    title = models.CharField(max_length=200)
    text = WYSIWYGField(null="True", blank="True")
   
    url_prefix = models.CharField(max_length=200, blank="True")
    url_prefix_needed = models.BooleanField(default=True)
    
    #article_template = models.CharField(max_length=200, blank="True")
    #article_template_own = models.BooleanField(default=True)
    
    specials = models.ManyToManyField(ArticleTypeSpecial, null="True", blank="True")
    
    def __unicode__(self):
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
    
    def __init__(self, *args, **kwargs):
        # получаем обьект профайла
        #self.prof = kwargs.get('instance', None)
        # в два поля нашей формы помещаем значения соотв.полей из модели user
         #kwargs['initial'] = {'sites': ArticleSpecial.objects.all(), }
        #kwargs.initial.__dict__['sites'] = ArticleSpecial.objects.all()
        #print "---Article----"
        #print kwargs.get('instance', None)
        super(FlatPage, self).__init__( *args, **kwargs)
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
            #print self.__dict__['template_name']
        #super(FlatPage, self).fields['sites'].initial = ArticleSpecial.objects.all()
    
    #def __init__(self, *args, **kwargs):
    #    super(FlatPage,self).__init__(*args, **kwargs)
        #super(FlatPage,self).__dict__['sites_default'] = ArticleSpecial.objects.all()
        #if self.atype
