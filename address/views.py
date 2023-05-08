from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import Response, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from address.models import Address
from address.serializers import AddressSerializer
from address.permissions import AdminOrOwnerPermission, IsAdmin

from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from accounts.models import Account

# Create your views here.
class AddressView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated()]

    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def list(self, serializer):
        AdminOrOwnerPermission().has_object_permission(self.request, Address, serializer)
        serialized = self.get_serializer_class()
        returned_information = serialized(self.get_queryset(), many=True)
        return Response(returned_information.data, status.HTTP_200_OK)
    
    @extend_schema(
        operation_id="address_list",
        responses={200: AddressSerializer},
        description="Rota de listagem de todos os endereços cadastrados",
        summary="Lista todos os endereços",
        tags=["Rotas de Address"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        operation_id="address_create",
        responses={201: AddressSerializer},
        description="Rota de criação de endereço, é obrigatório as propriedades: 'street', 'cep', 'number'",
        summary="Cria um endereço",
        tags=["Rotas de Address"],
    )
    def post(self, request, *args, **kwargs):
        serialized = self.serializer_class(data=request.data)
        serialized.is_valid(raise_exception=True)
        find_address = Address.objects.filter(**serialized.validated_data)
        if find_address:
            return Response(
                { "message": "Endereço já registrado." },
                status.HTTP_409_CONFLICT
            )

        find_user = Account.objects.filter(id=self.request.user.id).first()
        if find_user.address:
            return Response(
                { "message": "Usuário já possui um endereço cadastrado." },
                status.HTTP_409_CONFLICT
            )
        
        saved_info = serialized.save(account=find_user)
        serialized_return = self.serializer_class(instance=saved_info)
        find_user.address = saved_info
        find_user.save()
        return Response(serialized_return.data, status.HTTP_201_CREATED)

class AddressByIdView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AdminOrOwnerPermission]

    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    lookup_url_kwarg = "address_id"

    @extend_schema(
        operation_id="address_list_by_id",
        responses={200: AddressSerializer},
        parameters=[
                AddressSerializer,
                OpenApiParameter("address_id", OpenApiTypes.UUID, OpenApiParameter.PATH)
            ],
        description="Rota de listagem de um usuário, apenas o admin ou o proprio usuário pode acessar essa rota",
        summary="Lista um endereço especificado pelo ID",
        tags=["Rotas de Address"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @extend_schema(
        operation_id="address_put",
        responses={200: AddressSerializer},
        parameters=[
                AddressSerializer,
                OpenApiParameter("address_id", OpenApiTypes.UUID, OpenApiParameter.PATH)
            ],
        description="Altera totalmente as informações do endereço, apenas o admin ou o proprio usuário pode acessar essa rota",
        summary="Rota permite fazer uma alteração em um endereço através do ID passado pelo parâmetro 'address_id",
        tags=["Rotas de Address"],
    )
    def put(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @extend_schema(
        operation_id="address_patch",
        responses={200: AddressSerializer},
        parameters=[
                AddressSerializer,
                OpenApiParameter("address_id", OpenApiTypes.UUID, OpenApiParameter.PATH)
            ],
        description="Rota de listagem criação de endereço",
        summary="Altera parcialmente as informações do endereço, apenas o admin ou o proprio usuário pode acessar essa rota",
        tags=["Rotas de Address"],
    )
    def patch(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @extend_schema(
        operation_id="address_delete",
        responses={204: None},
        parameters=[
                OpenApiParameter("address_id", OpenApiTypes.UUID, OpenApiParameter.PATH)
            ],
        description="Rota permite deletar um endereço através do ID passado pelo parâmetro 'address_id",
        summary="Deleta um endereço, apenas o admin ou o proprio usuário pode acessar essa rota",
        tags=["Rotas de Address"],
    )
    def delete(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)