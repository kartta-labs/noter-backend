"""
Copyright 2020 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from noter_backend.settings import *
from distutils.util import strtobool
import sys

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('NOTER_BACKEND_SECRET_KEY', 'n%n&-x^t7)60331uvy#stf-s20dvxd*m2^m3bvwjfh!m=11=sb')
print('SECRET_KEY: {}'.format(SECRET_KEY))

# SECURITY WARNING: don't run with debug turned on in production!
NOTER_BACKEND_DEBUG = os.environ.get('NOTER_BACKEND_DEBUG', False)
if isinstance(NOTER_BACKEND_DEBUG, str):
  print('NOTER_BACKEND_DEBUG was a string')
  NOTER_BACKEND_DEBUG = bool(strtobool(NOTER_BACKEND_DEBUG))
DEBUG = NOTER_BACKEND_DEBUG
print('DEBUG: {}'.format(DEBUG))

ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True
MIDDLEWARE.insert(0, 'main.middleware.DevXEmailMiddleware')

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'main.authentication.NoCsrfSessionAuthentication',
        'rest_framework.authentication.BasicAuthentication'
    )
}

sys.stdout.flush()
