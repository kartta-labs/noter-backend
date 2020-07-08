from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # This backend is supposed to run behind a oauth proxy that puts
        # the authenticated user's email in X-EMAIL header. 
        return obj.owner.email == request.user.email


class IsOwnerOrRefuse(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or see it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner.email == request.user.email
