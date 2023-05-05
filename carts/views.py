from rest_framework import generics, permissions, exceptions
from rest_framework_simplejwt.authentication import JWTAuthentication
from . import models, serializers
from products.models import Product
from django.shortcuts import get_object_or_404
import ipdb

class CartDetailView(generics.RetrieveAPIView):
	authentication_classes = [JWTAuthentication]
	permission_classes = [permissions.IsAuthenticated]
	
	queryset = models.Cart.objects.all()
	serializer_class = serializers.CartSerializer
	pagination_class = None

	def get_object(self):
		account_id = self.request.user.id
		cart = self.queryset.get(account_id=account_id)

		return cart

class CartProductView(generics.CreateAPIView):
	authentication_classes = [JWTAuthentication]
	permission_classes = [permissions.IsAuthenticated]

	queryset = models.CartProduct.objects.all()
	serializer_class = serializers.CartProductSerializer

	def perform_create(self, serializer):
		product_id = self.kwargs.get('product_id')
		product = get_object_or_404(Product, id=product_id)
		
		if product.quantity < self.request.data['quantity']:
			raise exceptions.ValidationError({'message': 'Quantity is greater than the product amount in stock'})
		
		account_id = self.request.user.id
		cart = models.Cart.objects.get(account_id=account_id)
		serializer.save(cart_id=cart.id, product_id=product_id)
