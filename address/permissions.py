from rest_framework import permissions

class AdminOrOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if (request.user.is_superuser or obj.account == request.user):
            return True
        
class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser