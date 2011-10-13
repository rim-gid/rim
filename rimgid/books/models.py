from django.db import models

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
    text = models.TextField()
    text_full = models.TextField()
    
    cost = models.CharField(max_length=30)
    
    #map_address = models.CharField(max_length=2000)
    #map_preview = models.CharField(max_length=30)
    map_address = models.TextField()
    map_preview = models.TextField()
    
    def __unicode__(self):
        return self.title
    
class Tab(models.Model):
    adress = models.CharField(max_length=200)
    text = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.text
        
class Note(models.Model):
    title = models.CharField(max_length=200)
    #text = models.CharField(max_length=1000)
    text = models.TextField()
    date = models.DateField()
    image = models.CharField(max_length=50)
    
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
    hello_text = models.TextField()
    image = models.CharField(max_length=50)
    image_title = models.CharField(max_length=200)
    fon_image = models.CharField(max_length=50)
 
    def __unicode__(self):
        return self.title
 
class SiteFooter(models.Model):
    #text = models.CharField(max_length=1000)
    text = models.TextField()

    def __unicode__(self):
        return self.text

class Recomendations(models.Model):
    name = models.CharField(max_length=100)
    mail = models.CharField(max_length=100)
    image = models.CharField(max_length=50)
    #text = models.CharField(max_length=1000)
    text = models.TextField()
    date = models.DateField()

    def __unicode__(self):
        return self.name

class Shops(models.Model):
    title = models.CharField(max_length=200)
    #text = models.CharField(max_length=1000)
    text = models.TextField()
    image = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.title

class Transport(models.Model):
    title = models.CharField(max_length=200)
    #text = models.CharField(max_length=1000)
    text = models.TextField()
    image = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.title
        
class Transfer(models.Model):
    title = models.CharField(max_length=200)
    #text = models.CharField(max_length=1000)
    text = models.TextField()
    image = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.title        
        
