# -*- coding: utf-8 -*-
from django.forms.widgets import Textarea
from rimgid.wysiwyg import WidgetWYSIWYG

from django.forms import Textarea
from settings import MEDIA_URL

class WithImageWysiwygWidget(Textarea):
    def __init__(self, *args, **kwargs):
        super(WidgetWYSIWYG, self).__init__(attrs={'class': 'wysiwygEditor'}, *args, **kwargs)
    class Media:
        js = (
            MEDIA_URL+'wysiwyg/tiny_mce/tiny_mce.js',
            MEDIA_URL+'wysiwyg/textareas.js',
            )
        
    def render(self, name, value, attrs=None):
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        return mark_safe(u'<textarea%s>%s</textarea>' % (flatatt(final_attrs),
                conditional_escape(force_unicode(value))))