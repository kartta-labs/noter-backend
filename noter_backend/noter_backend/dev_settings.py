from noter_backend.settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True
MIDDLEWARE.insert(0, 'main.middleware.DevXEmailMiddleware')

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'main.authentication.NoCsrfSessionAuthentication',
        'rest_framework.authentication.BasicAuthentication'
    )
}
