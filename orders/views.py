from rest_framework import generics
from .serializers import OrderSerializer	
from .models import Order, ProductOrder
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from utils.sendEmail import send_html
from accounts.models import Account
from accounts.permissions import IsSeller
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError

from django.forms.models import model_to_dict
from orders.permissions import isAdminOrSeller

from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

class OrderView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated(), isAdminOrSeller()]
        return [IsAuthenticated()]
    
    pagination_class=PageNumberPagination
    queryset=Order.objects.all()
    serializer_class=OrderSerializer

    def perform_create(self, serializer):
        send_html(self.request.user.email, "Pending")
        user = self.request.user
        serializer.save(user=user)

        order_id = serializer.data["id"]
        if not model_to_dict(user.cart)["products"]:
             raise ValidationError({"messsage": "Cart está vazio."})
        products = user.cart.products.get_queryset()

        for product in products:
            ProductOrder.objects.create(order_id=order_id, product=product,\
                                        quantity=user.cart.cart_products.select_related().get(product_id=product.id).quantity)
            
        user.cart.products.set([])
        user.save()

    @extend_schema(
        operation_id="order_list",
        responses={200: OrderSerializer},
        description="Rota de listagem de pedidos de compra",
        summary="Lista todos os pedidos de compra",
        tags=["Rotas de Orders"]
    )
    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().get(self, request, *args, **kwargs)

        find_orders = Order.objects.filter(prodcuts__seller=self.request.user.id)
        queryset = self.paginate_queryset(find_orders)
        serialized = OrderSerializer(queryset, many=True)
        return self.get_paginated_response(serialized.data)
    
    @extend_schema(
        operation_id="order_create",
        description="Rota de criação de pedidos de compra",
        summary="Cria um pedido de compra",
        tags=["Rotas de Orders"],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
class OrderViewDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSeller]

    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def perform_update(self, serializer):
        order_pk=self.kwargs['pk']
        order_obj= Order.objects.get(id=order_pk)
        user_email=Account.objects.get(id=order_obj.user_id).email
        send_html(user_email,self.request.data['status'])
        
        serializer.save()

    @extend_schema(
        operation_id="order_list_by_id",
        responses={200: OrderSerializer},
        parameters=[
                OrderSerializer,
                OpenApiParameter("pk", OpenApiTypes.UUID, OpenApiParameter.PATH)
            ],
        description="Rota de listagem de um pedido de compra, apenas o vendedor possui acesso a rota",
        summary="Lista um pedido de compra específico",
        tags=["Rotas de Orders"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(self, request, *args, **kwargs)
    
    @extend_schema(
        operation_id="order_put",
        responses={200: OrderSerializer},
        parameters=[
                OrderSerializer,
                OpenApiParameter("pk", OpenApiTypes.UUID, OpenApiParameter.PATH)
            ],
        description="Rota permite fazer uma alteração em uma ordem de compra, apenas o vendedor possui acesso a rota",
        summary="Altera totalmente as informações da ordem de compra, apenas o vendedor possui acesso a rota",
        tags=["Rotas de Orders"],
    )
    def put(self, request, *args, **kwargs):
        return super().put(self, request, *args, **kwargs)
    
    @extend_schema(
        operation_id="order_patch",
        responses={200: OrderSerializer},
        parameters=[
                OrderSerializer,
                OpenApiParameter("pk", OpenApiTypes.UUID, OpenApiParameter.PATH)
            ],
        description="Rota permite fazer uma alteração em uma ordem de compra, apenas o vendedor possui acesso a rota",
        summary="Altera parcialmente as informações da ordem de compra, apenas o vendedor possui acesso a rota",
        tags=["Rotas de Orders"],
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(self, request, *args, **kwargs)
    
    @extend_schema(
        operation_id="order_delete",
        responses={204: None},
        parameters=[
                OpenApiParameter("id", OpenApiTypes.UUID, OpenApiParameter.PATH)
            ],
        description="Rota permite deletar uma ordem de compra, apenas o vendedor possui acesso a rota",
        summary="Deleta uma ordem de compra, apenas o vendedor possui acesso a rota",
        tags=["Rotas de Orders"],
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(self, request, *args, **kwargs)
		
class OrderInAccountView(generics.ListAPIView):
	authentication_classes = [JWTAuthentication]
	permission_classes = [IsAuthenticated]

	queryset = Order.objects.all()
	serializer_class = OrderSerializer

	def get_queryset(self):
		orders = self.queryset.filter(user_id=self.request.user.id)
		
		return orders