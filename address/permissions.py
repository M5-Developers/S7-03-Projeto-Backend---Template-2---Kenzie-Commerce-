from rest_framework import permissions

class AdminOrOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or obj == request.user:
            return True