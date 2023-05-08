from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from . import models, serializers

from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

class ProductView(generics.ListCreateAPIView):
	authentication_classes = [JWTAuthentication]
	permission_classes = [IsAuthenticatedOrReadOnly]
	
	queryset = models.Product.objects.all()
	serializer_class = serializers.ProductSerializer

	def perform_create(self, serializer):
		serializer.save(seller_id=self.request.user.id)
	
	def get_queryset(self):
		queryset = super().get_queryset()

		name = self.request.GET.get('name')
		category = self.request.GET.get('category')
		
		if name:
			queryset = queryset.filter(name__icontains=name)
			return queryset

		if category:
			queryset = queryset.filter(category__icontains=category)
		
		return queryset
	
	@extend_schema(
		operation_id="products_list",
		responses={200: serializers.ProductSerializer},
		description="Rota de listagem de todos os produtos",
		summary="Lista todos os produtos",
		tags=["Rotas de Products"]
	)
	def get(self, request, *args, **kwargs):
		return super().get(request, *args, **kwargs)
	
	@extend_schema(
		operation_id="product_create",
		responses={200: serializers.ProductSerializer},
		description="Rota de criação de um produto, é obrigatório as propriedades: 'name', 'category', 'price', 'quantity', caso a quantidade é 0, a propriedade 'avaliable' será False",
		summary="Cria um produto",
		tags=["Rotas de Products"]
	)
	def post(self, request, *args, **kwargs):
		return super().post(request, *args, **kwargs)

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
	authentication_classes = [JWTAuthentication]
	permission_classes = [IsAuthenticatedOrReadOnly]
	
	queryset = models.Product.objects.all()
	serializer_class = serializers.ProductSerializer

	@extend_schema(
		operation_id="product_by_id",
		responses={200: serializers.ProductSerializer},
		description="Rota de listagem de um produto ",
		summary="Lista um produto especificado pelo ID",
		tags=["Rotas de Products"]
	)
	def get(self, request, *args, **kwargs):
		return super().get(request, *args, **kwargs)
	
	@extend_schema(
		operation_id="product_put",
		responses={200: serializers.ProductSerializer},
		description="Altera totalmente as informações do produto",
		summary="Rota permite fazer uma alteração em um produto através do ID",
		tags=["Rotas de Products"]
	)
	def put(self, request, *args, **kwargs):
		return super().put(request, *args, **kwargs)
	
	@extend_schema(
		operation_id="product_patch",
		responses={200: serializers.ProductSerializer},
		description="Altera parcial as informações do produto",
		summary="Rota permite fazer uma alteração em um produto através do ID",
		tags=["Rotas de Products"]
	)
	def patch(self, request, *args, **kwargs):
		return super().patch(request, *args, **kwargs)
	
	@extend_schema(
		operation_id="product_delete",
		responses={204: None},
		description="Rota de deleção de um produto",
		summary="Rota permite deletar um produto especificado pelo ID",
		tags=["Rotas de Products"]
	)
	def delete(self, request, *args, **kwargs):
		return super().delete(request, *args, **kwargs)