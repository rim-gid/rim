# -*- coding: utf-8 -*-
from django import template
import views, settings, random
from rimgid import articles
import settings

register = template.Library()

"""
@register.tag(name="articles_list")
def do_articles_list(parser, token):
    try:
        tag_name, name = token.split_contents()
    except ValueError:
        msg = 'Тег %r требует один аргумент' % token.split_contents()[0]
        raise template.TemplateSyntaxError(msg)
    return ArticlesListResult(name[1:-1])
    
class ArticlesListResult(template.Node):
    def __init__(self, name):
        self.name = str(name)
        
    def render(self, context):
        try: 
            ar = articles_list(self.name)
        except:
            ar = ""
        return ar
"""
        
@register.simple_tag
def articles_list(token):
    try: 
        return views.articles_list(token)
    except:
        return ""

TEMP_ARTICLE_TITLE = ""

@register.simple_tag
def set_article_title(token):
    print "set_article_title", token
    global TEMP_ARTICLE_TITLE
    TEMP_ARTICLE_TITLE = token
    return ""

"""
@register.simple_tag
def articles_view(token):
    try: 
        return views.articles_list(token,"articles/articles_list_view.html")
    except:
        return ""
"""

@register.filter(name="articles_view")
def do_articles_view(token):
    try: 
        return views.articles_list(token,"articles/articles_list_view.html",order_by="-datetime")
    except:
        return ""

@register.filter(name="fotos_view")
def do_fotos_view(token):
    try: 
        return views.fotos_list(order_by="-datetime",url=token)
    except:
        return ""

@register.filter(name="special")
def do_special(node, arg):
    try:
        sp = node.specials.get(name=arg)
        res = sp.text
    except:
        res = ""
    return res
    
"""
{{ article|special_string:"style=\"height:50;background-image: url('/((button_image))');\"" }}
@register.filter(name="special_string")
def do_special_string(node, arg):
    arg
    try:
        sp = node.specials.get(name=arg)
        res = sp.text
    except:
        res = ""
    return res
"""

@register.inclusion_tag("articles/article_preview.html")
def last_article(type_name):
    print "random_article", type_name
    try:
        ar = articles.models.ArticleType.objects.get(title=type_name)
        ar_set = ar.article_set.filter(sites__id=settings.SITE_ID)
        #count = ar_set.count()
        article = ar_set[ar_set.count()-1] #article = ar_set[-1]
        #article = ar.article_set.all()[count-1]
        return {'article': article}
    except:
        return {'article': False}

@register.inclusion_tag("articles/article_preview.html")
def random_article(type_name):
    #print "random_article", type_name
    try:
        ar = articles.models.ArticleType.objects.get(title=type_name)
        ar_set = ar.article_set.filter(sites__id=settings.SITE_ID)
        count = ar_set.count()
        rand_num = random.randint(0, count-1)
        article = ar_set[rand_num]
        return {'article': article}
    except:
        return {'article': False}
