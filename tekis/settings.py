# -*- encoding: utf-8 -*-

import os

_ = lambda s: s

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY',
                       '=335vbnv-yq=zqk67=%wj38a2p71m029gx&zy0yr7bve9$zi13').strip('\"')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', False)

# Allowed hosts. WARNING: In production use, please use only the domain name as an allowed host, not an asterisk!
ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    # second party apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third party apps
    'django_markup',
    'easy_thumbnails',
    'oauth2_provider',
    'corsheaders',

    # first party apps
    'tekis.flatpages.apps.FlatpagesConfig',
    'tekis.members',
    'tekis.board.apps.BoardConfig',
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
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'tekis.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "tekis", "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'tekis.context_processors.site',
            ],
        },
    },
]

MARKUP_CHOICES = (
    'textile',
    'none',
    'linebreaks',
)

TOP_LEVEL, ASSOCIATION, ACTIVITIES = range(3)
FLATPAGES_MENU_CATEGORIES = (
    (ASSOCIATION, _("Association")),
    (ACTIVITIES, _("Activities")),
    (TOP_LEVEL, _("(Top level)")),
)
FLATPAGES_DEFAULT_MENU_CATEGORY = TOP_LEVEL

WSGI_APPLICATION = 'tekis.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'members': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'members.sqlite3'),
    }
}
DATABASE_ROUTERS = ['tekis.members.routers.MembersRouter']
AUTHENTICATION_BACKENDS = ['tekis.members.backends.TekisAuthBackend']
LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "/login/"

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en'
LANGUAGES = [
    ('fi', _(u"Finnish")),
    ('en', _(u"English")),
]

TIME_ZONE = 'Europe/Helsinki'
USE_I18N = True
USE_L10N = True
USE_TZ = True
LOCALE_PATHS = (os.path.join(BASE_DIR, "tekis", "locale"), )

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "public", "static")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
MEDIA_URL = '/files/'
MEDIA_ROOT = os.path.join(BASE_DIR, "public", "files")

# Thumbnail shapes
# https://github.com/SmileyChris/easy-thumbnails/blob/master/docs/usage.rst
THUMBNAIL_ALIASES = {
    '': {
        _('small'): {
            'size': (250, 250)
        },
        _('banner'): {
            'size': (960, 350),
            'crop': "smart"
        }
    },
}

# Cross Origin Resource Sharing headers for all oauth endpoints allows
# cross-origin POST requests
CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r'^/oauth/(authorize|token|revoke_token)/$'

SITE_NAME = os.getenv('SITE_NAME', 'TKO-äly ry').strip('\"')
SITE_URL = os.getenv('SITE_URL', 'http://localhost:8000').strip('\"')
BASE_TEMPLATE = "base_retro.html"
