from django.conf.urls.defaults import *

urlpatterns = patterns('',\
        ################################ Main dash forms
        (r'^$', 'records.views.home'),
        (r'^volunteer/$', 'records.views.volunteer'),
        (r'^volunteer/change/(?P<id>\d+)/$', 'records.views.changeVol'),
        (r'^profile/$', 'records.views.profile'),
        (r'^family/$', 'records.views.family'),
        (r'^pickup/$', 'records.views.pickup'),
        (r'^students/add/$', 'records.views.addStudent'),
        (r'^students/$', 'records.views.addStudent'),
        (r'^students/change/(?P<id>\d+)/$', 'records.views.changeStudent'),
        (r'^guardians/$', 'records.views.guardians'),
        (r'^contacts/$', 'records.views.ecf'),

        ################################# Application Process
        (r'^apply/guardians/$', 'records.views.guardians'),
        (r'^apply/profile/$', 'records.views.profile'),
        (r'^apply/family/$', 'records.views.family'),
        (r'^apply/volunteer/$', 'records.views.volunteer'),
        (r'^apply/$', 'records.views.apply'),
        (r'^apply/questions/parent/(?P<id>\d+)/$', 'records.views.parent'),
        (r'^apply/questions/(?P<id>\d+)/$', 'records.views.questions'),
        (r'^apply/questions/mssq/(?P<id>\d+)/$', 'records.views.mssq'),
        (r'^apply/current/(?P<id>\d+)/$', 'records.views.current'),
        (r'^apply/complete/$', 'records.views.appcontinue'),
        (r'^apply/complete/(?P<id>\d+)/$', 'records.views.appcomplete'),

        ################################# Registraton and re-enrollment process
        (r'^register/$', 'records.views.register'),
        (r'^register/(?P<id>\d+)/$', 'records.views.registerStudent'),
        (r'^enroll/$', 'records.views.enroll'),
        (r'^enroll/(?P<id>\d+)/$', 'records.views.enrollStudent'),
)
