# -*- coding: utf-8 -*-
from django.forms.widgets import Textarea
from rimgid.wysiwyg import WidgetWYSIWYG
"""
class Textarea(Widget):
    def __init__(self, attrs=None):
        # The 'rows' and 'cols' attributes are required for HTML correctness.
        default_attrs = {'cols': '40', 'rows': '10'}
        if attrs:
            default_attrs.update(attrs)
        super(Textarea, self).__init__(default_attrs)

    def render(self, name, value, attrs=None):
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        return mark_safe(u'<textarea%s>%s</textarea>' % (flatatt(final_attrs),
                conditional_escape(force_unicode(value))))
"""

from django.forms import Textarea
from settings import MEDIA_URL

"""
class WidgetWYSIWYG(Textarea):
    def __init__(self, *args, **kwargs):
        super(WidgetWYSIWYG, self).__init__(attrs={'class': 'wysiwygEditor'}, *args, **kwargs)
    class Media:
        js = (
            MEDIA_URL+'wysiwyg/tiny_mce/tiny_mce.js',
            MEDIA_URL+'wysiwyg/textareas.js',
            )
"""

class WithImageWysiwygWidget(Textarea):
    def __init__(self, *args, **kwargs):
        super(WidgetWYSIWYG, self).__init__(attrs={'class': 'wysiwygEditor'}, *args, **kwargs)
    class Media:
        js = (
            MEDIA_URL+'wysiwyg/tiny_mce/tiny_mce.js',
            MEDIA_URL+'wysiwyg/textareas.js',
            )
    #image_widget = 
  
    #def __init__(self, attrs=None):
    #    super(WithImageWysiwygWidget, self).__init__(attrs)
    #pass
    #def render(self, name, value, attrs=None):
    #    super(WithImageWysiwygWidget, self).render(name, value, attrs)# + "HELLO!"
        
    def render(self, name, value, attrs=None):
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        return mark_safe(u'<textarea%s>%s</textarea>' % (flatatt(final_attrs),
                conditional_escape(force_unicode(value))))