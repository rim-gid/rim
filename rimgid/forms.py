# -*- coding: utf-8 -*-
from django import forms
import datetime
#import floppyforms as forms
from settings import get_main_params

"""
import datetime, re  
from time import strptime  
  
from django.forms.widgets import Widget, Select  
from django.utils.dates import MONTHS, MONTHS_3  
from django.utils.safestring import mark_safe  
  
PATTERNS = (  
    ('%b', 'month'),  
    ('%B', 'month'),  
    ('%d', 'day'),  
    ('%m', 'month'),  
    ('%y', 'year'),  
    ('%Y', 'year'),  
)  
  
class SelectDateWidget(Widget):  
     
    #Extended version of django.newforms.extras.SelectDateWidget 
 
    #The main advantages are: 
    #- Widget can splits date input into custom select boxes. 
    #- Custom select boxes can have first empty option. 
      
    day_field = '%s_day'  
    month_field = '%s_month'  
    year_field = '%s_year'  
  
    def __init__(self, *args, **kwargs):  
         
        #Optional arguments: 
 
        #format_separator - separator in input_format. By default: - 
        #input_format     - valid date input format. By default: %B-%d-%Y 
        #null             - adds first empty option to all selects. By 
        #                   default: False 
        #years            - list/tuple of years to use in the "year" select 
        #                   box. By default: this year and next 9 printed. 
          
        self.attrs = kwargs.get('attrs', {})  
        self.format_separator = kwargs.get('format_separator', '-')  
        self.input_format = kwargs.get('input_format', '%B-%d-%Y')  
        self.null = kwargs.get('null', False)  
  
        if 'years' in kwargs:  
            self.years = kwargs['years']  
        else:  
            year = datetime.date.today().year  
            self.years = range(year, year+10)  
  
        fields = []  
        parts = self.input_format.split(self.format_separator)  
  
        for part in parts:  
            for k, v in PATTERNS:  
                if part == k:  
                    fields.append((k, v))  
  
        if not fields:  
            raise TypeError('Date input format "%s" is broken.' % self.input_format)  
  
        self.fields = fields  
        self.input_format = self.input_format.replace('%b', '%m').replace('%B', '%m')  
  
    def id_for_label(self, id_):  
        return id_  
    id_for_label = classmethod(id_for_label)  
  
    def render(self, name, value, attrs=None):  
        try:  
            year, month, day = value.year, value.month, value.day  
        except AttributeError:  
            year = month = day = None  
  
            if isinstance(value, basestring):  
                try:  
                    t = strptime(value, self.input_format)  
                    year, month, day = t[0], t[1], t[2]  
                except:  
                    pass  
  
        def _choices(pattern):  
            if pattern == '%b':  
                choices = MONTHS_3.items()  
                choices.sort()  
            elif pattern == '%B':  
                choices = MONTHS.items()  
                choices.sort()  
            elif pattern == '%d':  
                choices = [(i, i) for i in range(1, 32)]  
            elif pattern == '%m':  
                choices = [(i, i) for i in range(1, 13)]  
            elif pattern == '%y':  
                choices = [(i, str(i)[-2:]) for i in self.years]  
            elif pattern == '%Y':  
                choices = [(i, i) for i in self.years]  
  
            if self.null:  
                choices.insert(0, (None, mark_safe('&mdash;')))  
  
            return tuple(choices)  
  
        id_ = self.attrs.get('id', 'id_%s' % name)  
        output = []  
  
        for i, field in enumerate(self.fields):  
            pattern, field_name = field  
            field = getattr(self, '%s_field' % field_name)  
  
            sel_name = field % name  
            sel_value = locals().get(field_name, None)  
  
            if i == 0:  
                local_attrs = self.build_attrs(id=id_)  
            else:  
                local_attrs['id'] = field % id_  
  
            sel = Select(choices=_choices(pattern)).render(sel_name, sel_value, local_attrs)  
            output.append(sel)  
  
        return mark_safe('\n'.join(output))  
  
    def value_from_datadict(self, data, files, name):  
        value = []  
  
        for pattern, field_name in self.fields:  
            field = getattr(self, '%s_field' % field_name)  
            field_value = data.get(field % name, None)  
            if field_value and field_value != 'None':  
                value.append(str(field_value))  
  
        if value:  
            return '-'.join(value)  
  
        return data.get(name, None)  
"""

class ContactForm(forms.Form):
    mp = get_main_params()
    request_msg_error = mp['request_msg_error']
    request_title = mp['request_title']
    msg_thx = mp['msg_thx']
    name = forms.CharField(required=False,label=mp['form_label_name'],
      widget=forms.TextInput(attrs={'placeholder' : mp['form_input_name'], 'id' : 'order_name'},),)
    subject = forms.CharField(required=False,label=mp['form_label_date'],
      #initial=datetime.date.today,input_formats=('%d-%m-%Y',),
      #widget=SelectDateWidget(input_format='%d-%B-%Y', years=range(year, year-101, -1)),)
      widget=forms.TextInput(attrs={'placeholder' : mp['form_input_date'], 'id' : 'order_date'},),)
    email = forms.EmailField(required=True, label=mp['form_label_email'],widget=forms.TextInput(
      attrs={'placeholder' : mp['form_input_email'], 'id' : 'order_mail'},
      ),)
    message = forms.CharField(required=False, label=mp['form_label_comments'],widget=forms.Textarea(
      attrs={'placeholder' : mp['form_input_comments'], 'id' : 'order_text'},
      ),)