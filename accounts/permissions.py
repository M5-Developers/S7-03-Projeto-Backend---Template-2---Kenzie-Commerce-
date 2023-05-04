from rest_framework import permissions
from rest_framework.views import Request, View
from .models import Account


class IsAccountOnwer(permissions.BasePermission):
    def has_object_permission(
        self, request: Request, view: View, obj: Account
    ) -> bool:
        return request.user == obj
<<<<<<< HEAD
=======
    

class IsSeller(permissions.BasePermission):
	def has_permission(self, request:Request, view:View):
		if request.method in permissions.SAFE_METHODS:
			return True
		
		type:str=request.user.type.lower()
		return type=='seller' or type=='admin'
>>>>>>> 61ebf4919fce84ca7ee7e8d4a8d456612dbe7de4
