from django.conf.urls.defaults import *
from our_people import views as our_people_views

urlpatterns = patterns('',\
        url(r'^$', view=our_people_views.person_list, name='person_index'),
        (r'(?P<id>\d+)/$', 'our_people.views.detail'),
)

