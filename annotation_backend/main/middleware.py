from django.utils.deprecation import MiddlewareMixin

# This backend app runs behinds a proxy that sets the X-EMAIL header to
# the email of the authenticated user. In develpment mode, we may not want to 
# deal run behind a proxy. This middleware adds a default email to X-EMAIL
# header of the request to emulate the behaviour of the proxy.
class DevXEmailMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if 'HTTP_X_EMAIL' not in request.META:
            request.META['HTTP_X_EMAIL'] = "developer@example.com"