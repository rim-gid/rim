# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatpageForm
from django.utils.translation import ugettext_lazy as _
from django.forms.util import flatatt, ErrorDict, ErrorList
from models import *
from settings import MEDIA_URL
from decorators import PointedSaverSaveModel

class WysiwygAdmin(admin.ModelAdmin):
    """
    Класс, упрощающий замещение текстовых полей wysiwyg редактором
    """
    class Meta:
        # Список полей для которых нужно включить визуальный редактор    
        wysiwyg_fields = ()
  
    # Добавляем класс wysiwyg для всех полей перечисленных в Meta.wysiwyg_fields
    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(WysiwygAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in self.Meta.wysiwyg_fields:
            field.widget.attrs['class'] = 'wysiwygEditor'
        return field
  
    #formfield_overrides = {
    #    models.TextField: {'widget': WYSIWYGField},
    #}
  
    # Подключение js/css
    class Media:
        js = (
            MEDIA_URL+'wysiwyg/tiny_mce/tiny_mce.js',
            MEDIA_URL+'wysiwyg/textareas.js',
            )

class ArticleForm(forms.ModelForm):
    """
    настраиваем форму редактирования статьи
    """
    url = forms.RegexField(label=_("URL"), max_length=100, regex=r'^[-\w/]+$',
        help_text = "Example: '/excursion_3'. Be carefull: 1) '/' is needed; 2) don't change url, once saved. 3) don't use url, once used.",
                    #_("Example: '/about/contact/'. Make sure to have leading"
                    #  " and trailing slashes."),
        error_message = _("This value must contain only letters, numbers,"
                          " underscores, dashes or slashes."))
    
    #image = forms.ImageField(initial="empty",label='Main image',help_text = "You can add main image by this button (or by specials),"
    #                                                         " but only here you will upload image to server.")
    
    #def save(self,*args,**kwargs):
    #    print "SAAAAVING Form"
    #    super(ArticleForm,self).save(*args,**kwargs)
    """
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False):
        print "ArticleForm __init__"
        print "errors:", error_class
        super(ArticleForm,self).__init__(data, files, auto_id, prefix, initial, error_class, label_suffix, empty_permitted)
    """

    class Meta:
        model = Article

@PointedSaverSaveModel
class ArticleAdmin(WysiwygAdmin):
    """
    Класс настройки интерфейса администратора модели Article.
    """
    form = ArticleForm
    fieldsets = (
        (None, {'fields': ( 'url', ('title', 'atype'), 'content', 'sites')}), #('sites', 'image'))}),
        (_('Advanced options'), {'classes': ('collapse',), 'fields': ('specials', ('enable_comments', 'registration_required'), 'template_name')}),
    )
    list_display = ('url', 'atype', 'title')
    list_filter = ('atype', 'enable_comments', 'registration_required')
    search_fields = ('url', 'title')
    filter_horizontal = ('specials',)
        
    def duplicate_model(self, request, obj, form, change):
        """
        Используется методом save_model, определенным в PointedSaverSaveModel. Добавляет
        данные для дублирования - из полей sites и specials
        """
        obj.user = request.user
        sites = []
        specials = []
        try:
            sites += request.POST.pop('sites')
        except:
            pass
        try:
            specials += request.POST.pop('specials')
        except:
            pass
        obj.save(duplicate=True,sites=sites,specials=specials)
    
    class Meta:
        wysiwyg_fields = ('content')
        
@PointedSaverSaveModel
class ArticleSpecialAdmin(WysiwygAdmin):
    """
    Класс настройки интерфейса администратора модели ArticleSpecial.
    """
    #form = ArticleForm
    fieldsets = (
        (None, {'fields': ( ('name', 'image'), 'text')}),
    )
    #list_display = ('url', 'atype', 'title')
    list_filter = ('name', 'text', 'image')
    search_fields = ('name', 'text', 'image')
        
    def duplicate_model(self, request, obj, form, change):
        """
        Используется методом save_model, определенным в PointedSaverSaveModel.
        """
        obj.user = request.user
        obj.save(duplicate=True)
    
    class Meta:
        wysiwyg_fields = ('content')

@PointedSaverSaveModel
class FotoAdmin(WysiwygAdmin):
    """
    Класс настройки интерфейса администратора модели ArticleSpecial.
    """
    #form = ArticleForm
    #fieldsets = (
    #    (None, {'fields': ( ('name', 'image'), 'text')}),
    #)
    #list_display = ('url', 'atype', 'title')
    #list_filter = ('name', 'text', 'image')
    #search_fields = ('name', 'text', 'image')
        
    def duplicate_model(self, request, obj, form, change):
        """
        Используется методом save_model, определенным в PointedSaverSaveModel.
        """
        sites = []
        try:
            sites += request.POST.pop('sites')
        except:
            pass
        obj.user = request.user
        obj.save(duplicate=True,sites=sites)
    
    class Meta:
        wysiwyg_fields = ('content')

admin.site.register(ArticleSpecial, ArticleSpecialAdmin)
admin.site.register(ArticleTypeSpecial)
admin.site.register(ArticleType)
admin.site.register(Foto, FotoAdmin)
admin.site.register(Article, ArticleAdmin)