from .base import *

LOGGING = LOGGING

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

if DEBUG:
    for logger in LOGGING["loggers"]:
        LOGGING["loggers"][logger]["level"] = "DEBUG"
else:
    for logger in LOGGING["loggers"]:
        LOGGING["loggers"][logger]["level"] = "INFO"

ALLOWED_HOSTS = ['*','localhost']

CORS_ALLOWED_ORIGINS = [
    'http://localhost:8000',
]

INSTALLED_APPS += ["debug_toolbar", "django_extensions"]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    "content-type",
    "authorization",
    "x-requested-with"
]

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]
WSGI_APPLICATION = "clipbuddy.asgi.dev.application"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DATABASE_NAME', 'clipbuddy'),
        'USER': os.getenv('DATABASE_USER', 'clipbuddy_user'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', 'clipbuddy_password'),
        'HOST': os.getenv('DATABASE_HOST', 'db'),
        'PORT': os.getenv('DATABASE_PORT', '5432'),
    }
}

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]