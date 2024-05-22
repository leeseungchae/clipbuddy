from .base import *

LOGGING = LOGGING

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

if DEBUG:
    for logger in LOGGING["loggers"]:
        LOGGING["loggers"][logger]["level"] = "DEBUG"
else:
    for logger in LOGGING["loggers"]:
        LOGGING["loggers"][logger]["level"] = "INFO"


ALLOWED_HOSTS = []

INSTALLED_APPS += ["debug_toolbar", "django_extensions"]

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]
WSGI_APPLICATION = "clipbuddy.asgi.dev.application"

DATABASES = DATABASES