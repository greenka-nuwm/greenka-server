from rest_framework import permissions


class IsTreeOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner


class IsTreeImageTreeOwner(permissions.BasePermission):
    """Check if user can attach image to tree"""

    def has_object_permission(self, request, view, obj):
        return obj.tree.owner == request.user