from annotation_backend.settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True
MIDDLEWARE += ['main.middleware.DevXEmailMiddleware']