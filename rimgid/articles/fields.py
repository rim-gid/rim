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

"""
class WithImageWysiwygField(WYSIWYGField):
  
    #image_field = ImageField(upload_to="images/")
    
    #def __init__(self, *args, **kwargs):
    #    self.max_length = kwargs.pop('max_length', None)
    #    super(FileField, self).__init__(*args, **kwargs)
  
    def formfield(self, **kwargs):
        defaults = {'widget': WithImageWysiwygWidget}
        defaults.update(kwargs)
        return super(WithImageWysiwygField, self).formfield(**defaults)
        
    #def to_python(self, data):
    #    f = super(WithImageWysiwygField,self).to_python(data)
        #f_im = image_field.to_python(data)
    #    return f #+ f_im
        
    #def clean(self, data, initial=None):
    #    return super(WithImageWysiwygField, self).clean(data) #+ image_field.clean(data)
        
        #if not data and initial:
        #    return initial
        #return super(FileField, self).clean(data)
"""
