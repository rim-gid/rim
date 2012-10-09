# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
import order, static
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    ('^/?contact_form(/(?P<ex>[^/]+))?/?$', order.contact_form),
    
    # админка------------------:
    (r'^admin/', include(admin.site.urls)),
    
    # заказ экскурсии------------------:
    ('^/?order_excursion/(?P<ex>\w+)/(?P<mail>\w+)/(?P<text>\w+)/?$', order.excursion_order),
    
    # статика ------------------:
    ('^/?(?P<name>\w+).css/?$', static.get_css),
    ('^/?rimgid/wysiwyg/(?P<name>[^.]+)\.(?P<tp>\w+)/?$', static.get_from_wysiwyg),
    ('^/?(?P<name>\w+).js/?$', static.get_js),
    ('^/?(images/)?((?P<papka>\w+)/)?(?P<name>[^/]+)\.(?P<tp>\w+)/?$', static.get_image),
    ('^/?ds_stamper.ttf/?$', static.get_image, {'tp':'ttf'}),
)

