from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

from django.views.generic.simple import redirect_to

from registration.forms import RegistrationFormUniqueEmail
from endpoint import Endpoint

from settings import DEBUG, PROJECT_DIR
import os

if DEBUG:
    urlpatterns = patterns('',\
            (r'^media/(?P<path>.*)$', 'django.views.static.serve',\
            {'document_root': os.path.join(PROJECT_DIR, 'media/')}),

            (r'^admin_media/(?P<path>.*)$', 'django.views.static.serve',\
            {'document_root': os.path.join(PROJECT_DIR, 'admin_media/')}),
    )
else:
    urlpatterns = patterns('',)

urlpatterns += patterns('',
    # This is the return url for processing the IPN for paypal
    (r'^endpoint/$', Endpoint(),),

    ################################# Registration
    (r'^accounts/profile/$', redirect_to, {'url':'/'}),
    (r'^accounts/register/$', 'registration.views.register',\
            {'form_class': RegistrationFormUniqueEmail},),
    (r'^accounts/', include('registration.urls')),

    ################################# Admin
    # Mail
    (r'^admin/(?P<app_label>[\d\w]+)/(?P<model_name>[\d\w]+)/mail/$',\
            'utils.mail',),
    # For export to csv
    (r'^admin/(?P<app_label>[\d\w]+)/(?P<model_name>[\d\w]+)/csv/$',\
            'utils.admin_list_export'),
    # For Printing
    (r'^admin/(?P<app_label>[\d\w]+)/(?P<model_name>[\d\w]+)/(?P<pk>[\d]+)/print/$',\
            'records.views.print_detail'),
    (r'^admin/(.*)', admin.site.root),

    ################ Parent Dashboard, Application and Enrollment
    (r'^records/', include('records.urls')),

    ################################### Menu urls
    (r'^menu/', include('menu.urls')),

    ############### Blog urls
    (r'blog/', include('blog.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),

    ################## Media_logs
    (r'videos/', include('media_logs.urls.videos')),
    (r'photos/', include('media_logs.urls.photos')),

    ########### our_people
    (r'our_people/', include('our_people.urls')),

    ######### Basic site views
    (r'^$', 'homeviews.home'),
    (r'^calendar/$', 'homeviews.calendar'),
)

