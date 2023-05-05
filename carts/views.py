from rest_framework import generics, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from . import models, serializers
import ipdb

class CartView(generics.RetrieveAPIView):
	authentication_classes = [JWTAuthentication]
	permission_classes = [permissions.IsAuthenticated]
	
	queryset = models.Cart.objects.all()
	serializer_class = serializers.CartSerializer
	pagination_class = None

	def get_object(self):
		account_id = self.request.user.id
		cart = self.queryset.get(account_id=account_id)
		ipdb.set_trace()
		return cart
