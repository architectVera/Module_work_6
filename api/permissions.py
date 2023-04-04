from rest_framework import permissions
from rest_framework.permissions import BasePermission, IsAuthenticated


class UserPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsOwnerOrAdmin(BasePermission):
    """Access right for purchase owner or administrator only"""
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.user == request.user
