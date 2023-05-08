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
		
		if self.request.data['quantity'] > product.quantity:
			raise exceptions.ValidationError({'message': 'Quantity is greater than the product amount in stock'})
		
		
		account_id = self.request.user.id
		cart = models.Cart.objects.get(account_id=account_id)


		cart_product = self.queryset.filter(cart_id=cart.id, product_id=product_id).first()

		if cart_product:
			if cart_product.quantity + self.request.data['quantity'] > product.quantity:
				raise exceptions.ValidationError({'message': 'Quantity is greater than the product amount in stock'})
			
			cart_product_serializer = serializers.CartProductSerializer(instance=cart_product, data=self.request.data, partial=True)
			cart_product_serializer.is_valid(raise_exception=True)

			return cart_product_serializer.save()

		serializer.save(cart_id=cart.id, product_id=product_id)

class CartProductDetailView(generics.UpdateAPIView):
	authentication_classes = [JWTAuthentication]
	permission_classes = [permissions.IsAuthenticated]

	queryset = models.CartProduct.objects.all()
	serializer_class = serializers.CartProductSerializer
	lookup_field = 'cart_id'

class CartProductDeleteView(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    queryset = models.CartProduct.objects.all()

    def get_object(self):
        cart_id = self.kwargs.get('cart_id')
        product_id = self.kwargs.get('product_id')
        account_id = self.request.user.id
        cart_product = self.queryset.filter(cart_id=cart_id, product_id=product_id, cart__account_id=account_id).first()
        return cart_product

    

