# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    #(r'^/?admin/', include(admin.site.urls)),
    
    ('^/?contact_form/?(?P<ex>[^/]+)/?$',contact_form),
    
    ('^/?robots.txt', robots),
    ('^/?yandex_61b9f126eb948082.txt', yandex_61b9f126eb948082_txt),
    ('^/?$', base_left_page, {'page_type':'main'}),
    ('^/?contacts/?$', base_left_page, {'page_type':'contacts'}),
    ('^/?transfer/?$', base_left_page, {'page_type':'transfer'}),
    ('^/?transport/?$', base_left_page, {'page_type':'transport'}),
    ('^/?shops/?$', base_left_page, {'page_type':'shops'}),
    ('^/?fotos/?$', base_left_page, {'page_type':'fotos'}),
    ('^/?notes/?$', base_left_page, {'page_type':'notes'}),
    ('^/?italy/?$', base_left_page, {'page_type':'italy'}),
    ('^/?translate/?$', base_left_page, {'page_type':'translate'}),
    ('^/?recomendations/?$', base_left_page, {'page_type':'recomendations'}),
    ('^/?excursion/(?P<num>\d+)/?$', excursion_page),
    ('^/?order_excursion/(?P<ex>\w+)/?(?P<mail>\w+)/?(?P<text>\w+)/?$', excursion_order),
    ('^/?ex_list.html', ex_list),
    
    ('^/?style.css/?$', get_css, {'name' : 'style'}),
    
    ('^/?(?P<name>\w+).htc/?$', get_htc),
    ('^/?(?P<name>\w+).png/?$', get_png),
    ('^/?(?P<name>\w+).jpg/?$', get_jpg),
    ('^/?(?P<name>\w+).pdf/?$', get_pdf),
    ('^/?images/(?P<name>\w+).png/?$', get_png),
    ('^/?images/(?P<name>\w+).jpg/?$', get_jpg),
    ('^/?images/(?P<papka>\w+)/(?P<name>\w+).jpg/?$', get_papka_jpg),
    
    ('^/?rim-kolizey-fon.png/$', get_png, {'name':'rim-kolizey-fon'}),
    ('^/?kolizey-2.jpg/$', get_jpg, {'name':'kolizey-2'}),
    ('^/?rim-kolizey-fon-small.png/$', get_png, {'name':'rim-kolizey-fon-small'}),
    ('^/?ex-li-fon-(?P<num>\d+).png/$', get_num_image_png, {'url':'ex-li-fon-'} ),
    ('^/?rim-fon-(?P<num>\d+).jpg/$', get_num_image_jpg, {'url':'rim-fon-'} ),

    ('^/?ds_stamper.ttf/$', get_ttf, {'name':'ds_stamper'}),
    
    ('[.]+',error404),
    
    # Examples:
    # url(r'^$', 'rimgid.views.home', name='home'),
    # url(r'^rimgid/', include('rimgid.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
#    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': '/path/to/media'}),
    #(r'^admin/', include(admin.site.urls)),
    (r'^admin/', include(admin.site.urls)),
    #(r'^/?admin/admin/$', include(admin_media)),
    #(r'^admin/admin/(?P<path>.*)$', 'django.views.static.serve',{'document_root': '/usr/local/www/rim/admin_media/', 'show_indexes': True}),
)

