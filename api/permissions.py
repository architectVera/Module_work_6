"""Description of permission classes."""

from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS


class UserPermission(permissions.BasePermission):
    """Permission class that only allows access to objects
    if the requesting user matches the object user."""

    def has_object_permission(self, request, view, obj):
        """Check if the requesting user matches the object user."""
        return obj == request.user


class IsOwnerOrAdmin(BasePermission):
    """Access right for purchase owner or administrator only"""

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.user == request.user


class SessionPermission(BasePermission):
    """ Custom permission class for SessionViewSet.
        Allows read access to everyone (for GET requests).
        Allows create, update, and delete access only to superusers.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            """Returns True if the user is a superuser for non-safe methods (POST, PUT, DELETE),
               otherwise returns True for safe methods (GET, HEAD, OPTIONS)."""
            return True
        else:
            return request.user.is_superuser
