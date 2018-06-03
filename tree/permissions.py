from rest_framework import permissions


class IsTreeOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        print(view)
        return request.user == obj.owner


class IsTreeImageTreeOwner(permissions.BasePermission):
    """Check if user can attach image to tree"""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsAdminOrReadOnly(permissions.IsAdminUser):
    """Everyone can view, but only admin edit."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return super(IsAdminOrReadOnly, self).has_permission(request, view)