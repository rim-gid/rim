# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import Template, Context
from django.shortcuts import render_to_response
from django.conf import settings
import datetime, os, time

# рендерит все заметки выбранной таблицы
def renderNotesText(objs):
    datas = objs.objects.all()
    for data in datas:
      data.text = renderText(data.text)
    return datas
    
# рендерит конкретную заметку
def renderNote(note):
    if note:
      note.text = renderText(note.text)
    return note

# рендерит конкретный текст
def renderText(text):
    if text:
      db_template = Template(text)
      text = Template('{% extends db_template %}').render(Context(locals()))
    return text