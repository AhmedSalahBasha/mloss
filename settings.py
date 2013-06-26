# Django settings for mloss project.

VERSION = "r0000"
PRODUCTION = False # set to True when project goes live

if not PRODUCTION:
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG
else:
    DEBUG = False

ADMINS = (
    ('Mikio Braun', 'mikio@cs.tu-berlin.de'),
    ('Cheng Soon Ong', 'chengsoon.ong@unimelb.edu.au'),
    ('Soeren Sonnenburg', 'soeren.sonnenburg@tu-berlin.de'),
)

MANAGERS = ADMINS

R_CRAN_BOT = 'r-cran-robot'

if PRODUCTION:
    DATABASES = {
        'default': {
            'USER': 'mloss',             # Not used with sqlite3.
            'PASSWORD': 'XXXXXXXXX',     # Not used with sqlite3.
            'HOST': '',             # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',             # Set to empty string for default. Not used with sqlite3.
            'ENGINE': 'django.db.backends.mysql',           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
            'NAME': 'mloss',             # Or path to database file if using sqlite3.
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
            'NAME': 'mloss.db',             # Or path to database file if using sqlite3.
        }
    }


LOGIN_REDIRECT_URL='/'
ACCOUNT_ACTIVATION_DAYS=1
DEFAULT_FROM_EMAIL='mloss@mloss.org'

# send email from this address
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# Local time zone for this installation. Choices can be found here:
# http://www.postgresql.org/docs/8.1/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
# although not all variations may be possible on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Berlin'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
if PRODUCTION:
    MEDIA_ROOT = '/home/mloss/static/media/'
else:
    MEDIA_ROOT = 'media/'

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = '/media/'

# max size of files that can be uploaded in KB (10M, 200K)
MAX_FILE_UPLOAD_SIZE = 10240
MAX_IMAGE_UPLOAD_SIZE = 200
MAX_IMAGE_UPLOAD_WIDTH = 1280
MAX_IMAGE_UPLOAD_HEIGHT = 1024

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
#ADMIN_MEDIA_PREFIX = '/media_admin/'
STATIC_URL = '/media_admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'ccku5%_-8r2#*rb(yh)j!11ar12vx_tll5u(11%3l=^k8rfe=y'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    )

ROOT_URLCONF = 'mloss.urls'


#import os.path
if PRODUCTION:
    TEMPLATE_DIRS = (
        '/home/mloss/django/mloss/templates/',
        )
else:    
    TEMPLATE_DIRS = (
        'templates/',
        )

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.comments',
    'django.contrib.markup',
    'django.contrib.syndication',
    'django.contrib.flatpages',
    'django.contrib.humanize',
    'mloss',
    'mloss.software',
    'mloss.revision',
    'mloss.registration',
    'mloss.community',
    'mloss.forshow',
    'mloss.user',
    'mloss.subscriptions',
    'mloss.aggregator',
    'mloss.blog',
    'mloss.captcha',
)

RECAPTCHA_PUBLIC_KEY = 'RECAPTCHAPUBLIC'
RECAPTCHA_PRIVATE_KEY = 'RECAPTCHAPRIVATE'

