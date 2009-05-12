import os, sys
sys.path.append('/home/skyl/proj')
sys.path.append('/home/skyl/proj/django-school')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
