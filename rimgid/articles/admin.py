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
            field.widget.attrs['class'] = 'wysiwygEditor'
        return field
  
    # Подключение js/css
    class Media:
        js = (
            MEDIA_URL+'wysiwyg/tiny_mce/tiny_mce.js',
            MEDIA_URL+'wysiwyg/textareas.js',
            )

class ArticleForm(forms.ModelForm):
    url = forms.RegexField(label=_("URL"), max_length=100, regex=r'^[-\w/]+$',
        help_text = _("Example: '/about/contact/'. Make sure to have leading"
                      " and trailing slashes."),
        error_message = _("This value must contain only letters, numbers,"
                          " underscores, dashes or slashes."))
                          
    image = forms.ImageField(initial='Do you want to add image?')
    
    #def save(self,*args,**kwargs):
    #    print "SAAAAVING Form"
    #    super(ArticleForm,self).save(*args,**kwargs)

    class Meta:
        model = Article

class ArticleAdmin(WysiwygAdmin):
    form = ArticleForm
    fieldsets = (
        (None, {'fields': ('url', 'title', 'atype', 'content', 'sites', 'image')}),
        (_('Advanced options'), {'classes': ('collapse',), 'fields': ('specials','enable_comments', 'registration_required', 'template_name')}),
    )
    list_display = ('url', 'atype', 'title')
    list_filter = ('atype', 'enable_comments', 'registration_required')
    search_fields = ('url', 'title')

class WysiwygFlatPageAdmin(ArticleAdmin, WysiwygAdmin):
    def save_model(self, request, obj, form, change):
        super(WysiwygFlatPageAdmin,self).save_model(request, obj, form, change)
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

admin.site.register(ArticleSpecial)
admin.site.register(ArticleTypeSpecial)
admin.site.register(ArticleType)
admin.site.register(Foto)
admin.site.register(Article, WysiwygFlatPageAdmin)