# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from rimgid.wysiwyg import WYSIWYGField

# Create your models here.
class Book(models.Model):
    name = models.CharField(max_length=50)
    pub_date = models.DateField()
    
    def __unicode__(self):
        return self.name

class Excursion(models.Model):
    title = models.CharField(max_length=200)
    title_time = models.CharField(max_length=50)
    
    button_image = models.CharField(max_length=50)
    
    group = models.CharField(max_length=20)
    special = models.CharField(max_length=100)
    
    #text = models.CharField(max_length=1000)
    #text_full = models.CharField(max_length=5000)
    text = WYSIWYGField()
    text_full = WYSIWYGField()
    
    cost = models.CharField(max_length=30)
    
    #map_address = models.CharField(max_length=2000)
    #map_preview = models.CharField(max_length=30)
    map_address = models.TextField()
    map_preview = models.TextField()
    
    def __unicode__(self):
        return self.title
        
class SiteParam(models.Model):
    name = models.CharField(max_length=200)
    value = models.TextField()
    def __unicode__(self):
        return self.name
    
class Tab(models.Model):
    adress = models.CharField(max_length=200)
    text = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.text
        
class Note(models.Model):
    title = models.CharField(max_length=200)
    #text = models.CharField(max_length=1000)
    text = WYSIWYGField()
    date = models.DateField()
    image = models.ImageField(upload_to="images/",null="True")
    
    def __unicode__(self):
        return self.title
        
class Contacts(models.Model):
    name = models.CharField(max_length=50) # phone, vkontakte, e-mail, address, skype
    value = models.CharField(max_length=100)
    image = models.CharField(max_length=200)
    c_type = models.CharField(max_length=30) # image, link, text, image_and_text, image_and_link

    def __unicode__(self):
        return self.name

class OlgaInfo(models.Model):
    title = models.CharField(max_length=50)
    #hello_text = models.CharField(max_length=1000)
    hello_text = WYSIWYGField()
    image = models.CharField(max_length=50)
    image_title = models.CharField(max_length=200)
    fon_image = models.CharField(max_length=50)
 
    def __unicode__(self):
        return self.title
 
class SiteFooter(models.Model):
    #text = models.CharField(max_length=1000)
    text = WYSIWYGField()

    def __unicode__(self):
        return self.text

class Reccomendations(models.Model):
    name = models.CharField(max_length=100)
    mail = models.CharField(max_length=100)
    #image = models.CharField(max_length=50)
    #text = models.CharField(max_length=1000)
    text = WYSIWYGField()
    image = models.ImageField(upload_to="images/",null="True")
    date = models.DateField()

    def __unicode__(self):
        return self.name

class Shops(models.Model):
    title = models.CharField(max_length=200)
    #text = models.CharField(max_length=1000)
    text = WYSIWYGField()
    image = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.title

class Transport(models.Model):
    title = models.CharField(max_length=200)
    #text = models.CharField(max_length=1000)
    text = WYSIWYGField()
    image = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.title
        
class Transfer(models.Model):
    title = models.CharField(max_length=200)
    #text = models.CharField(max_length=1000)
    text = WYSIWYGField()
    image = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.title        

class Fotos(models.Model):
    title = models.CharField(max_length=200)
    text = WYSIWYGField()
    #upload_to=settings.MEDIA_ROOT+
    image = models.ImageField(upload_to="images/",null="True")
    date = models.DateField()
    
    def __unicode__(self):
        return self.title    

class Flights(models.Model):
    title = models.CharField(max_length=200)
    text = WYSIWYGField()
    #upload_to=settings.MEDIA_ROOT+
    image = models.ImageField(upload_to="images/",null="True")
    #date = models.DateField()
    
    def __unicode__(self):
        return self.title        

class Hotels(models.Model):
    title = models.CharField(max_length=200)
    text = WYSIWYGField()
    #upload_to=settings.MEDIA_ROOT+
    image = models.ImageField(upload_to="images/",null="True")
    #date = models.DateField()
    
    def __unicode__(self):
        return self.title    
   
      
class Restaurants(models.Model):
    title = models.CharField(max_length=200)
    text = WYSIWYGField()
    #upload_to=settings.MEDIA_ROOT+
    image = models.ImageField(upload_to="images/",null="True")
    #date = models.DateField()
    
    def __unicode__(self):
        return self.title    
