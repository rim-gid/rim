# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.sites.models import Site
from settings import get_main_params

def PointedSaver(cls):
    """
    Декоратор модели для дублирования в дублирующую базу ("pointed") при сохранении.
    Добавляет в объект класса модели ряд методов, общих при дублировании.
    """
    def save(self, *args, **kwargs):
        """
        Если modelAdmin передала дополнительные значения для дублирования, то происходит дублирование,
        по-умолчанию происходит сохранение
        """
        if args or kwargs:
            print "----duplicating----"
            if "duplicate" in kwargs:
                del kwargs["duplicate"]
            duplicate_using(self,"pointed",*args,**kwargs)
        else:
            print "----saving----"
            super(cls,self).save(*args, **kwargs)
    
    def dublicate_me_using_base(resource,uss,**kwargs):
        """
        Сам объект дублируется, только если такого не найдено в дублирующей базе
        """
        try:
            obj = cls.objects.using(uss).get(**kwargs)
        except:
            obj = cls(**kwargs)
            super(cls,obj).save(using=uss)
        return obj
        #return cls.objects.using(uss).get_or_create(using=uss,**kwargs)
    
    def duplicate_using(resource,uss,*args,**kwargs):
        """
        Главный метод дублирования. Порядок следующий: сам объект, его параметры, сохранение.
        """
        obj = resource.dublicate_me_using(uss,**kwargs)
        resource.duplicate_objects_using(obj,uss,*args,**kwargs)
        super(cls,obj).save(using=uss)
        return obj
    
    def fill_sites(self,obj, uss, *args, **kwargs):
        """
        Дополнительная функция - объекту следует ее использовать для дублирования поля "sites"
        """
        if "sites" in kwargs:
            sites = kwargs["sites"]
            print sites
            for s in sites:
                try:
                    new_s = Site.objects.using(uss).get(id=int(s))
                except:
                    new_s = Site(name="new",domain="new",id=int(s))
                obj.sites.add(new_s)

    def fill_specials(self,sp_type, obj, uss, *args, **kwargs):
        """
        Дополнительная функция - объекту следует ее использовать для дублирования поля "specials"
        """
        if "specials" in kwargs:
            specials = kwargs["specials"]
            print specials
        for s in self.specials.all():
            new_s, created = sp_type.objects.using(uss).get_or_create(name=s.name,text=s.text)
            obj.specials.add(new_s)
        
    cls.save = save
    cls.duplicate_using = duplicate_using
    cls.fill_sites = fill_sites
    cls.fill_specials = fill_specials
    cls.dublicate_me_using_base = dublicate_me_using_base
    return cls
    
def PointedSaverSaveModel(cls):
    """
    Декоратор переопределяет метод ModelAdmin.save_model для дублирования данных в связанную БД
    """
    def save_model(self, request, obj, form, change):
        """
        При сохранении добавляем параметры для дублирования,
        если не задано не использовать дублирование.
        """
        mp = get_main_params()
        if 'no_saving' in mp['local']:
            if mp['local']['no_saving']:
                return
        #print "request:", request
        super(cls,self).save_model(request, obj, form, change)
        if 'no_duplicating' in mp['local']:
            if mp['local']['no_duplicating']:
                return
        self.duplicate_model(request, obj, form, change)
  
    cls.save_model = save_model
    return cls