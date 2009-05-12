from django.conf.urls.defaults import *
urlpatterns = patterns('',\
        (r'^$', 'menu.views.see'),
        url(r'^(?P<studentid>\d+)/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$',\
                'menu.views.order', name='place_order'),
        (r'^cancel/(?P<studentid>\d+)/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$',\
                'menu.views.cancel'),
        (r'^paynow/(?P<id>\d+)/$', 'menu.views.paynow'),
)
