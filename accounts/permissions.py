from rest_framework import permissions
from rest_framework.views import Request, View
from .models import Account

class IsAccountOnwer(permissions.BasePermission):
    def has_object_permission(
        self, request: Request, view: View, obj: Account
    ) -> bool:
        return request.user == obj
    

class IsSeller(permissions.BasePermission):
    def has_permission(self, request, view):
        type:str=request.user.type
        if type.lower()=='seller':
            return True
        return False