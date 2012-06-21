# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from rimgid.wysiwyg import WYSIWYGField
from django.contrib.flatpages.models import FlatPage

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
        return self.title

class ArticleTypeSpecial(ArticleSpecial):
    stype = "articleType"

class ArticleType(models.Model):
    title = models.CharField(max_length=200)
    text = WYSIWYGField(null="True", blank="True")
   
    url_prefix = models.CharField(max_length=200, blank="True")
    url_prefix_needed = models.BooleanField(True)
    
    specials = models.ManyToManyField(ArticleTypeSpecial, null="True", blank="True")
    
    def __unicode__(self):
        return self.title

class Foto(models.Model):
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    text = WYSIWYGField(blank="True")
    image = models.ImageField(upload_to="fotos/",null="True", blank="True")
    datetime = models.DatetimeField(blank="True")
    
    stype = "article"
    
    def __unicode__(self):
        return self.title

class Article(FlatPage):
    atype = models.ForeignKeyField(ArticleType)
    specials = models.ManyToManyField(ArticleSpecial, null="True", blank="True")
    
    datetime = models.DatetimeField(blank="True")
    
    #def __unicode__(self):
    #    return self.title