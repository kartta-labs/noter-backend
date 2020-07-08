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
