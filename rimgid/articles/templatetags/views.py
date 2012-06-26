# -*- coding: utf-8 -*-
from django.template import Template, Context
from django.template.loader import get_template
from django.conf import settings
from rimgid.articles.models import Article

def articles_list(name,template="articles/articles_list.html"):
    """
    вывод списка статей по типу
    """
    articles = Article.objects.filter(
                    atype__title__exact = name, #фильтруется по atype.title
                    sites__id__exact=settings.SITE_ID
                ).order_by('id')
    t = get_template(template)
    return t.render(Context({'articles': articles}))