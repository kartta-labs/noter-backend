"""
Provides authentication policies.
"""
from rest_framework.authentication import BaseAuthentication, BasicAuthentication, SessionAuthentication


class NoCsrfSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        """
        Pass CSRF validation. This should be used only in dev mode.
        """
        pass