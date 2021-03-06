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


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'n%n&-x^t7)60331uvy#stf-s20dvxd*m2^m3bvwjfh!m=11=sb'

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
