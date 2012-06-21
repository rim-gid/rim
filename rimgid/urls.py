# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    ('^/?contact_form(/(?P<ex>[^/]+))?/?$',contact_form),
    
    # PAGES---------------:
    # для яндекса------------------:
    ('^/?robots.txt', robots),
    ('^/?yandex_61b9f126eb948082.txt', yandex_61b9f126eb948082_txt),
    ('^/?1be09f3f8a74.html', html_1be09f3f8a74_html),
    # для яндекса end------------------:
    
    # админка------------------:
    (r'^admin/', include(admin.site.urls)),
    (r'^/?admin_excursions/?$',edit_excursions),
    # админка end------------------:
    
    # общие страницы------------------:
    ('^/?$', get_page, {'page_type':'main'}),
    ('^/?(?P<page_type>\w+)?/?$', get_page),
    # общие страницы end------------------:
    
    # экскурсии------------------:
    ('^/?excursion/(?P<num>\d+)/?$', excursion_page),
    ('^/?order_excursion/(?P<ex>\w+)/(?P<mail>\w+)/(?P<text>\w+)/?$', excursion_order),
    #('^/?ex_list.html', ex_list),
    # экскурсии end------------------:
    # PAGES end---------------:
    
    # STATIC------------------:
    ('^/?(?P<name>\w+).css/?$', get_css),
    ('^/?(?P<name>\w+).js/?$', get_js),
    ('^/?(images/)?((?P<papka>\w+)/)?(?P<name>[^/]+)\.(?P<tp>\w+)/?$', get_image),
    ('^/?ds_stamper.ttf/$', get_image, {'tp':'ttf'}),
    # STATIC end------------------:
    
)

