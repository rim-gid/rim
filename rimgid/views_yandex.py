# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse

def robots(request):
    return render_to_response('robots.txt', locals())
    
def yandex_61b9f126eb948082_txt(request):
    return render_to_response('yandex_61b9f126eb948082.txt', locals())
    
def html_1be09f3f8a74_html(request):
    return render_to_response('1be09f3f8a74.html', locals())