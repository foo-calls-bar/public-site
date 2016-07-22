import os

HTML_MINIFY             = False
DEBUG                   = True
#SECURE_SSL_REDIRECT     = True
SESSION_COOKIE_SECURE   = True
CSRF_COOKIE_SECURE      = True
#SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
PROJECT_NAME            = 'agcs'
BASE_DIR         = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_URLCONF     = PROJECT_NAME + '.urls'
EMAIL_USE_TLS    = True
ADMINS           = (('Ryan Kaiser', 'ryank@alphageek.xyz'),)
MANAGERS         = ADMINS
WSGI_APPLICATION = PROJECT_NAME +'.wsgi.application'
LANGUAGE_CODE    = 'en-us'
TIME_ZONE        = 'America/Chicago'
USE_I18N         = True
USE_L10N         = True
USE_TZ           = True
STATIC_URL       = '/static/'
STATIC_ROOT      = os.path.join('/var/tmp', PROJECT_NAME, 'assets', 'static')
STATICFILES_DIRS = [
    ('assets', os.path.join(BASE_DIR, PROJECT_NAME, 'static'))
]
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         'LOCATION': '127.0.0.1:11211',
#     }
# }
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',
    'django.contrib.sitemaps',
    'favicon',
    'snowpenguin.django.recaptcha2',
    'landing.apps.LandingConfig',
    'bootstrap3',
    'django_assets',
]
MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, PROJECT_NAME, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.request',
            ],
        },
    },
]

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

COMPANY = {
    'phone'      : '(972) 656-9338',
    'email'      : 'root@alphageek.xyz',
    'addr'       : ['1727 Nest Pl.', 'Plano, TX 75093'],
    'long_name'  : 'Alpha Geek Computer Services',
    'short_name' : 'Alpha Geeks',
    'links' : {
        'social' : {
            'facebook'    : 'https://facebook.com/alphageekcs',
            'google_plus' : 'https://plus.google.com/+Ntxcomputerservices',
            'google_maps' : 'https://maps.google.com?daddr=Alpha+Geek+Computer+Services+1727+Nest+Place+Plano+TX+75093'
        },
    },
}

#GOOGLE_API_KEY = ''
#SECRET_KEY = ''
#EMAIL_HOST = ''
#EMAIL_PORT = ''
#EMAIL_HOST_USER = ''
#EMAIL_HOST_PASSWORD = ''
#DATABASES = {}
#RECAPTCHA_PRIVATE_KEY = ''
#RECAPTCHA_PUBLIC_KEY = ''

try:
    from .local_settings import *
except ImportError:
    pass

from django.contrib.staticfiles.storage import staticfiles_storage


ANDROID_ICONS=[
    {
        'density': '0.75',
        'sizes': '36x36',
        'src': staticfiles_storage.url('assets/img/android-chrome-36x36.png'),
        'type': 'image/png'
    },
    {
        'density': '1.0',
        'sizes': '48x48',
        'src': staticfiles_storage.url('assets/img/android-chrome-48x48.png'),
        'type': 'image/png'
    },
    {
        'density': '1.5',
        'sizes': '72x72',
        'src': staticfiles_storage.url('assets/img/android-chrome-72x72.png'),
        'type': 'image/png'
    },
    {
        'density': '2.0',
        'sizes': '96x96',
        'src': staticfiles_storage.url('assets/img/android-chrome-96x96.png'),
        'type': 'image/png'
    },
    {
        'density': '3.0',
        'sizes': '144x144',
        'src': staticfiles_storage.url('assets/img/android-chrome-144x144.png'),
        'type': 'image/png'
    },
    {
        'density': '4.0',
        'sizes': '192x192',
        'src': staticfiles_storage.url('assets/img/android-chrome-192x192.png'),
        'type': 'image/png'
    },
]

SECRET_KEY = '&qaeg(mBecauseitsmandatoryv@@n$if67ba-4e9&kk+j$$c+'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
