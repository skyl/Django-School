from django.conf.urls.defaults import *
from media_logs.models import *


audio_list = {
  'queryset': Audio.objects.all(),
}
audio_set_list = {
  'queryset': AudioSet.objects.all(),
}


urlpatterns = patterns('',
  url(
    regex   = '^sets/(?P<slug>[-\w]+)/$',
    view    = 'django.views.generic.list_detail.object_detail',
    kwargs  = audio_set_list,
    name    = 'audio_set_detail',
  ),
  url (
    regex   = '^sets/$',
    view    = 'django.views.generic.list_detail.object_list',
    kwargs  = audio_set_list,
    name    = 'audio_set_list',
  ),
  url(
    regex   = '^(?P<user>[-\w]+)/(?P<slug>[-\w]+)/$',
      #regex   = '^(?P<slug>[-\w]+)/$',
    view    = 'views.generic.list_detail.object_detail',
    kwargs  = audio_list,
    name    = 'audio_detail',
  ),
  url (
    regex   = '^$',
    view    = 'django.views.generic.list_detail.object_list',
    kwargs  = audio_list,
    name    = 'audio_list',
  ),
)
