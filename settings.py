# -*- coding: utf-8 -*-
import os
from shrine.init import dj_database_url

DEBUG = not os.getenv("PORT")
TEMPLATE_DEBUG = DEBUG
PRODUCTION = not DEBUG

ADMINS = (
    (u"gabrielfalcao", "gabrielfalcao@codervana.io"),
)

MANAGERS = ADMINS
PRODUCT_NAME = "codervana"
APP_EMAIL_ADDRESS = "emailer@codervana.io"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'codervana',
        'USER': 'codervana',
        'PASSWORD': 'C0D3RV4N4',
        'HOST': 'mysql.gabrielfalcao.com',
        'PORT': '',
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB',
        },
    }
}

if not PRODUCTION:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': './codervana.sqlite',
        }
    }


TEMPLATE_PATH = "./templates"
STATIC_PATH = "./media"

INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
)
DOMAIN = "app.codervana.io"
if not PRODUCTION:
    DOMAIN = "localhost:8000"

AUTHENTICATED_HOME = "/"
ANONYMOUS_HOME = "/"

ENV_NAME = "localhost"

TORNADO_CONFIG = {
    'login_url': '/login',
    'cookie_secret': "25e5503bca667e4989f0272f4f57853143baa73d83362280c3cce155bf65e348e0be022371a33050cbaa81e9b124851997f079f4cbfa001e79981e2f99001bf6",
}


if PRODUCTION:
    EMAIL_BACKEND = "shrine.mailgun.EmailBackend"
    ENV_NAME = "codervana_production"

MAKE_FULL_URL = lambda x: "http://{0}/{1}".format(DOMAIN, x.lstrip("/"))
