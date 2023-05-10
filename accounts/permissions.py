from rest_framework import permissions
from rest_framework.views import Request, View
from .models import Account


class IsAccountOnwer(permissions.BasePermission):
    def has_object_permission(
        self, request: Request, view: View, obj: Account
    ) -> bool:
        return request.user == obj


class IsSeller(permissions.BasePermission):
    def has_permission(self, request:Request, view):
        print(request)
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method=='PUT' or request.method=='PATCH':
            return request.user.is_staff
        if request.path=='/api/products/' and request.method=='POST':
            return request.user.is_staff

        return True