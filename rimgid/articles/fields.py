# -*- coding: utf-8 -*-
from rimgid.wysiwyg import WYSIWYGField
from django.forms.fields import ImageField, Field
from widgets import WithImageWysiwygWidget

class WithImageWysiwygField(Field):
    def get_internal_type(self):
        return "TextField"

    def formfield(self, **kwargs):
        defaults = {'widget': WithImageWysiwygWidget}
        defaults.update(kwargs)
        return super(WithImageWysiwygField, self).formfield(**defaults)

