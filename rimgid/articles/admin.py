# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin
from rimgid.articles.models import *
from settings import MEDIA_URL
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatpageForm
from django.utils.translation import ugettext_lazy as _

class WysiwygAdmin(admin.ModelAdmin):
    class Meta:
        # Список полей для которых нужно включить визуальный редактор    
        wysiwyg_fields = ()
  
    # Добавляем класс wysiwyg для всех полей перечисленных в Meta.wysiwyg_fields
    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(WysiwygAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in self.Meta.wysiwyg_fields:
            field.widget.attrs['class'] = 'wysiwygEditor'#'wysiwyg ' + field.widget.attrs.get('class', '')
            
        #def __init__(self, *args, **kwargs):
        #super(WidgetWYSIWYG, self).__init__(attrs={'class': 'wysiwygEditor'}, *args, **kwargs)
            
        return field
  
    # Подключение js/css
    class Media:
        js = (
            MEDIA_URL+'wysiwyg/tiny_mce/tiny_mce.js',
            MEDIA_URL+'wysiwyg/textareas.js',
            )
            
        #js = ('http://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js',
        #      settings.MEDIA_URL + 'js/wymeditor/jquery.wymeditor.pack.js',
        #      settings.MEDIA_URL + 'js/wysiwyg.js',)
  
        #css = {'screen': (settings.MEDIA_URL + 'js/wymeditor/skins/default/screen.css',)}

"""
class TimeSheetEntryAdmin(admin.ModelAdmin):
    
    list_filter = ['employee', 'status', ActiveCompaniesFilter, ...,
'project__company']


class SitesFilter(SimpleListFilter):
    title = _('active companies')
    parameter_name = 'project__company__id'
   def lookups(self, request, model_admin):
        lookup_list = Company.objects.active().values_list('id',
'name').distinct()
        return lookup_list

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(project__company=self.value())
"""


class ArticleForm(forms.ModelForm):
    url = forms.RegexField(label=_("URL"), max_length=100, regex=r'^[-\w/]+$',
        help_text = _("Example: '/about/contact/'. Make sure to have leading"
                      " and trailing slashes."),
        error_message = _("This value must contain only letters, numbers,"
                          " underscores, dashes or slashes."))

    class Meta:
        model = Article

class ArticleAdmin(WysiwygAdmin):#FlatPageAdmin,
    form = ArticleForm
    fieldsets = (
        (None, {'fields': ('url', 'title', 'atype', 'content', 'sites')}),
        (_('Advanced options'), {'classes': ('collapse',), 'fields': ('specials','enable_comments', 'registration_required', 'template_name')}),
    )
    list_display = ('url', 'atype', 'title')
    list_filter = ('atype', 'enable_comments', 'registration_required')
    search_fields = ('url', 'title')

class WysiwygFlatPageAdmin(ArticleAdmin, WysiwygAdmin):#FlatPageAdmin,  
  
    class Meta:
        wysiwyg_fields = ('content')

#admin.site.unregister(FlatPage)
#admin.site.register(FlatPage, WysiwygFlatPageAdmin) 


"""
from django.db import models
from rimgid.wysiwyg import WYSIWYGField
 
admin.site.unregister(models.TextField)
admin.site.register(models.TextField, WYSIWYGField)
"""

admin.site.register(ArticleSpecial)
admin.site.register(ArticleTypeSpecial)
admin.site.register(ArticleType)
admin.site.register(Foto)
admin.site.register(Article, WysiwygFlatPageAdmin)