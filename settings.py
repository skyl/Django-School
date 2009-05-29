import os
PROJECT_DIR = os.path.dirname(__file__)

DEBUG = False
TEMPLATE_DEBUG = DEBUG
LIVE = True


ADMINS = (
    ('Skylar Saveland', 'skylar.saveland@gmail.com'),
)

MANAGERS = ADMINS

if not LIVE:
    DATABASE_ENGINE = 'sqlite3'
    DATABASE_NAME = os.path.join(PROJECT_DIR, 'dev.db')
else:
    from local_settings import DATABASE_ENGINE, DATABASE_NAME, DATABASE_USER,\
        DATABASE_PASSWORD, DATABASE_HOST, DATABASE_PORT

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True

MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')

if not LIVE:
    MEDIA_URL = '/media/'
    ADMIN_MEDIA_PREFIX = '/admin_media/'
else:
    from local_settings import MEDIA_URL, ADMIN_MEDIA_PREFIX

from local_settings import SECRET_KEY

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware', )

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.markup',
    'comments',
    'registration',         # easy_install django-registration
    'template_utils',       # easy_install django-template-utils
    #    'djangogcal',           # put on svn version on python path
    'tagging',
    'blog',
    'media_logs',
    'people',
    'records',
    'menu',
    'years',
    'payments',
    'our_people',
)

AUTHENTICATION_BACKENDS = (
    'email-auth.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
)

from local_settings import EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD,\
    EMAIL_PORT, DEFAULT_FROM_EMAIL, SERVER_EMAIL

AUTH_PROFILE_MODULE = 'records.userprofile'
ACCOUNT_ACTIVATION_DAYS = 7

