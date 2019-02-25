from rest_framework import permissions


class IsFeedbackImageOwner(permissions.BasePermission):
    """Check if user can attach image to feedback"""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsFeedbackOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner
