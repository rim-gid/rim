# -*- coding: utf-8 -*-
from django import forms
import datetime
from templatetags.project_options import get_project_option

class ContactForm(forms.Form):
    #mp = get_main_params()
    request_msg_error = get_project_option('request_msg_error')
    request_title = get_project_option('request_title')
    msg_thx = get_project_option('msg_thx')
    name = forms.CharField(
      required = False,
      label = get_project_option('form_label_name'),
      widget = forms.TextInput(
        attrs = {
          'placeholder' : get_project_option('form_input_name'),
          'id' : 'order_name'
        },
      ),
    )
    subject = forms.CharField(
      required = False,
      label = get_project_option('form_label_date'),
      widget = forms.TextInput(
        attrs = {
          'placeholder' : get_project_option('form_input_date'),
          'id' : 'order_date'
        },
      ),
    )
    email = forms.EmailField(
      required = True,
      label = get_project_option('form_label_email'),
      widget = forms.TextInput(
        attrs = {
          'placeholder' : get_project_option('form_input_email'),
          'id' : 'order_mail'
        },
      ),
    )
    message = forms.CharField(
      required = False,
      label = get_project_option('form_label_comments'),
      widget = forms.Textarea(
        attrs = {
          'placeholder' : get_project_option('form_input_comments'),
          'id' : 'order_text'
        },
      ),
    )

