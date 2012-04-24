# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    #(r'^/?admin/', include(admin.site.urls)),

    (r'^/?admin_jseditor/?$', jseditor),
    
    ('^/?contact_form/?(?P<ex>[^/]+)/?$',contact_form),
    
    # PAGES:
    ('^/?robots.txt', robots),
    ('^/?yandex_61b9f126eb948082.txt', yandex_61b9f126eb948082_txt),
    ('^/?1be09f3f8a74.html', html_1be09f3f8a74_html),
    
    ('^/?$', get_page, {'page_type':'main'}),
    ('^/?(?P<page_type>\w+)?/?$', get_page),
    
    ('^/?excursion/(?P<num>\d+)/?$', excursion_page),
    ('^/?order_excursion/(?P<ex>\w+)/?(?P<mail>\w+)/?(?P<text>\w+)/?$', excursion_order),
    ('^/?ex_list.html', ex_list),
    
    ('^/?test.html', test),
    
    # IMAGES:
    ('^/?(?P<name>\w+).css/?$', get_css),
    ('^/?(?P<name>\w+).js/?$', get_js),
    ('^/?(images/)?((?P<papka>\w+)/)?(?P<name>[^/]+)\.(?P<tp>\w+)/?$', get_image),
    ('^/?ds_stamper.ttf/$', get_image, {'tp':'ttf'}),
    
    #('^/?[.]+/?$',error404),
    
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
    (r'^/?admin_excursions/?$',edit_excursions),
    #(r'^/?admin/admin/$', include(admin_media)),
    #(r'^admin/admin/(?P<path>.*)$', 'django.views.static.serve',{'document_root': '/usr/local/www/rim/admin_media/', 'show_indexes': True}),
)

