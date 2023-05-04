from rest_framework import permissions
from rest_framework.views import Request, View
from .models import Account


class IsAccountOnwer(permissions.BasePermission):
    def has_object_permission(
        self, request: Request, view: View, obj: Account
    ) -> bool:
        return request.user == obj
    

class IsSeller(permissions.BasePermission):
	def has_permission(self, request:Request, view:View):
		if request.method in permissions.SAFE_METHODS:
			return True
		
		type:str=request.user.type.lower()
		return type=='seller' or type=='admin'
