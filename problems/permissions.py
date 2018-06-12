from rest_framework import permissions


class IsAdminOrReporterOrReadOnly(permissions.IsAdminUser):
    """Everyone can view, but only admin edit."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if obj.reporter == request.user:
            return True
        return super(IsAdminOrReporterOrReadOnly, self).has_object_permission(request, view, obj)