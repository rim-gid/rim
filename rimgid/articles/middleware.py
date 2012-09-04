# -*- coding: utf-8 -*-
from models import FlatPage
from views import article
from django.contrib.flatpages.middleware import FlatpageFallbackMiddleware
from django.http import Http404
from django.conf import settings

class ArticleFallbackMiddleware(FlatpageFallbackMiddleware):
    """
    класс используется для использования вместо объекта FlatPage объекта Article
    """
    def process_response(self, request, response):
        if response.status_code != 404:
            return response
        try:
            return article(request, request.path_info)
        except Http404:
            return response
        except:
            if settings.DEBUG:
                raise
            return response