# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from rimgid.wysiwyg import WYSIWYGField
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
import datetime


class ProjectOption(models.Model):
    #LANGUAGE_CHOICES = (
    #    ('all','All'),
    #    ('ru-RU','Russian'),
    #    ('en-US','English'),
    #)
    name = models.CharField(max_length=200)
    value = WYSIWYGField(blank="True")
    sites = models.ManyToManyField(Site)
    #language = models.CharField(default="all",max_length=6,choices=LANGUAGE_CHOICES)
    
    def get_sites(self):
        return '; '.join([s.name for s in self.sites.all()])
    
    def __unicode__(self):
        return self.name + " ["+str(self.get_sites())+"]" + " = " + self.value
        
