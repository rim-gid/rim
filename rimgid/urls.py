from django.conf.urls.defaults import patterns, include, url
from views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    ('^/?robots.txt', robots),
    ('^/?$', base_left_page, {'page_type':'main'}),
    ('^/?contacts/?$', base_left_page, {'page_type':'contacts'}),
    ('^/?transfer/?$', base_left_page, {'page_type':'transfer'}),
    ('^/?transport/?$', base_left_page, {'page_type':'transport'}),
    ('^/?notes/?$', base_left_page, {'page_type':'notes'}),
    ('^/?recomendations/?$', base_left_page, {'page_type':'recomendations'}),
    ('^/?excursion/(?P<num>\d+)/?$', excursion_page),
    ('^/?ex_list.html', ex_list),
    
    ('^/?style.css/?$', get_css, {'name' : 'style'}),
    
    #('^/?olga.png/$', get_png, {'name':'olga'}),
    ('^/?rim-kolizey-fon.png/$', get_png, {'name':'rim-kolizey-fon'}),
    ('^/?kolizey-2.jpg/$', get_jpg, {'name':'kolizey-2'}),
    ('^/?rim-kolizey-fon-small.png/$', get_png, {'name':'rim-kolizey-fon-small'}),
    ('^/?(?P<name>\w+).png/?$', get_png),

    ('^/?ex-li-fon-(?P<num>\d+).png/$', get_num_image_png, {'url':'ex-li-fon-'} ),
    ('^/?rim-fon-(?P<num>\d+).jpg/$', get_num_image_jpg, {'url':'rim-fon-'} ),

    ('^/?(?P<name>\w+).jpg/?$', get_jpg),
    ('^/?e-mail.png/$', get_png, {'name':'e-mail'}),
    
    #('^fon.png/$', get_png, {'name':'fon'}),
    #('^vk.png/$', get_png, {'name':'vk'}),
    ('^fon_orange.png/$', get_png, {'name':'fon_orange'}),
    ('^/?ds_stamper.ttf/$', get_ttf, {'name':'ds_stamper'}),
    # Examples:
    # url(r'^$', 'rimgid.views.home', name='home'),
    # url(r'^rimgid/', include('rimgid.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
#    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': '/path/to/media'}),
    (r'^admin/', include(admin.site.urls)),
)
