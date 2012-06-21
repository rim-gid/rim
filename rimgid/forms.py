# -*- coding: utf-8 -*-
from django import forms
import datetime
from settings import get_main_params

class ContactForm(forms.Form):
    mp = get_main_params()
    request_msg_error = mp['request_msg_error']
    request_title = mp['request_title']
    msg_thx = mp['msg_thx']
    name = forms.CharField(
      required = False,
      label = mp['form_label_name'],
      widget = forms.TextInput(
        attrs = {
          'placeholder' : mp['form_input_name'],
          'id' : 'order_name'
        },
      ),
    )
    subject = forms.CharField(
      required = False,
      label = mp['form_label_date'],
      widget = forms.TextInput(
        attrs = {
          'placeholder' : mp['form_input_date'],
          'id' : 'order_date'
        },
      ),
    )
    email = forms.EmailField(
      required = True,
      label = mp['form_label_email'],
      widget = forms.TextInput(
        attrs = {
          'placeholder' : mp['form_input_email'],
          'id' : 'order_mail'
        },
      ),
    )
    message = forms.CharField(
      required = False,
      label = mp['form_label_comments'],
      widget = forms.Textarea(
        attrs = {
          'placeholder' : mp['form_input_comments'],
          'id' : 'order_text'
        },
      ),
    )