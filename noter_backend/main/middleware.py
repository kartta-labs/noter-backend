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

from django.contrib import auth
from django.contrib.auth.models import User
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject


# This backend app runs behinds a proxy that sets the X-EMAIL header to
# the email of the authenticated user. In develpment mode, we may not want to 
# deal run behind a proxy. This middleware adds a default email to X-EMAIL
# header of the request to emulate the behaviour of the proxy.
class DevXEmailMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if 'HTTP_X_EMAIL' not in request.META:
            request.META['HTTP_X_EMAIL'] = "developer@example.com"


def get_or_create_authenticated_user(request):
    email = request.META.pop('HTTP_X_EMAIL', None)
    if not email:
        return None
    if not User.objects.filter(email=email).exists():
        user = User.objects.create_user(email, email, email)
        user.save()
    return User.objects.get(email=email)

def get_user(request):
    if not hasattr(request, '_cached_user'):
        request._cached_user = get_or_create_authenticated_user(request)
    return request._cached_user


class OAuthProxyAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        assert hasattr(request, 'session'), (
            "The OAuth Proxy authentication middleware requires session middleware "
            "to be installed. Edit your MIDDLEWARE setting to insert "
            "'django.contrib.sessions.middleware.SessionMiddleware' before "
            "'main.OAuthProxyAuthenticationMiddleware'."
        )

        request.user = SimpleLazyObject(lambda: get_user(request))
