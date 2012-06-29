# -*- coding: utf-8 -*-
from django.template import Template, Context
from django.template.loader import get_template
from django.conf import settings
from rimgid.articles.models import Article, Foto
import settings

def articles_list(name,template="articles/articles_list.html",order_by='id'):
    """
    вывод списка статей по типу
    """
    try:
        sp = name.split("|")
        name = sp[0]
        template = sp[1]
    except:
        pass
    articles = Article.objects.filter(
                    atype__title__exact = name, #фильтруется по atype.title
                    sites__id__exact=settings.SITE_ID
                ).order_by(order_by)
                
    #print name, " count = ", str(len(articles))
                
    t = get_template(template)
    return t.render(Context({'articles': articles}))
    
def fotos_list(template="articles/fotos_view.html",order_by='id',url=""):
    """
    вывод фотографий
    """
    fotos = Foto.objects.filter(
                    sites__id__exact=settings.SITE_ID
                ).order_by(order_by)
    fotos
    t = get_template(template)
    ft_titles = [u'Фото','Photos'] #FIXME вшито использование SITE_ID
    ft_title = ft_titles[settings.SITE_ID-1]
    return t.render(Context({'fotos': fotos,'type_url': url, 'type_title': ft_title}))