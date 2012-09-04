# -*- coding: utf-8 -*-
from django import template
from models import ProjectOption
import settings

register = template.Library()

@register.tag(name="project_option")
def do_project_option(parser, token):
    try:
        tag_name, name = token.split_contents()
    except ValueError:
        msg = 'Тег %r требует один аргумент' % token.split_contents()[0]
        raise template.TemplateSyntaxError(msg)
    return ProjectOptionResult(name[1:-1])
    
def get_project_option(name):
    try:
        pr = ProjectOption.objects.filter(
            name__exact = name,
            sites__id__exact = settings.SITE_ID
        )
        pr = pr[0].value
    except:
        pr = ""
    return pr
    
class ProjectOptionResult(template.Node):
    def __init__(self, name):
        self.name = str(name)
        
    def render(self, context):
        return get_project_option(self.name)