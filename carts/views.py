from rest_framework import generics, permissions, exceptions
from rest_framework_simplejwt.authentication import JWTAuthentication
from . import models, serializers
from products.models import Product
from django.shortcuts import get_object_or_404
import ipdb

from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

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

	@extend_schema(
		operation_id="carts_list",
		responses={200: serializers.CartSerializer},
		description="Rota de listagem de todos os carrinhos",
		summary="Lista todos os carrinhos",
		tags=["Rotas de Carts"]
	)
	def get(self, request, *args, **kwargs):
		return super().get(request, *args, **kwargs)

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

	@extend_schema(
		operation_id="cart_create",
		responses={200: serializers.CartProductSerializer},
		description="Rota de criação de carrinho ou adição de item no carrinho",
		summary="Cria um carrinho e/ou adiciona um produto dentro do mesmo",
		tags=["Rotas de Carts"]
	)
	def post(self, request, *args, **kwargs):
		return super().post(request, *args, **kwargs)

class CartProductDetailView(generics.UpdateAPIView):
	authentication_classes = [JWTAuthentication]
	permission_classes = [permissions.IsAuthenticated]

	queryset = models.CartProduct.objects.all()
	serializer_class = serializers.CartProductSerializer
	lookup_field = 'cart_id'

	@extend_schema(
		operation_id="cart_update",
		responses={200: serializers.CartProductSerializer},
		parameters=[
                serializers.CartProductSerializer,
                OpenApiParameter("cart_id", OpenApiTypes.UUID, OpenApiParameter.PATH)
            ],
		description="Rota de atualização de um carrinho",
		summary="Atualiza um carrinho especificado pelo ID",
		tags=["Rotas de Carts"]
	)
	def patch(self, request, *args, **kwargs):
		return super().patch(request, *args, **kwargs)