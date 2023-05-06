from accounts.permissions import IsAccountOnwer
from .serializers import AccountSerializer
from .models import Account
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes


# MRO - Method Resolution Order
class AccountView(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    @extend_schema(
        operation_id="accounts_list",
        responses={200: AccountSerializer},
        description="Rota de listagem de contas de usuários, qualquer usuário possui acesso a essa informação",
        summary="Listagem de todos os usuários",
        tags=["Rotas de Accounts"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @extend_schema(
        operation_id="accounts_create",
        responses={201: AccountSerializer},
        parameters=[AccountSerializer],
        description="Rota de criação de contas de usuários, ",
        summary="Criação de usuário",
        tags=["Rotas de Accounts"],
    )
    def post(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class AccountDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountOnwer]

    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    lookup_url_kwarg = "account_id"

    @extend_schema(
        operation_id="accounts_list_by_id",
        responses={200: AccountSerializer},
        description="Rota de listagem de um usuário, apenas o proprio usuário pode acessar essa rota",
        summary="Lista um usuário especificado pelo ID",
        tags=["Rotas de Accounts"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @extend_schema(
            operation_id="accounts_put",
            responses={200: AccountSerializer},
            parameters=[
                AccountSerializer,
                OpenApiParameter("account_id", OpenApiTypes.UUID, OpenApiParameter.PATH)
            ],
            summary="Altera totalmente as informações do usuário, apenas o proprio usuário pode fazer alteração na sua conta",
            description="Rota permite fazer uma alteração em um usuário através do ID passado pelo parâmetro 'account_id'",
            tags=["Rotas de Accounts"]
    )
    def put(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @extend_schema(
            operation_id="accounts_patch",
            responses={200: AccountSerializer},
            parameters=[
                AccountSerializer,
                OpenApiParameter("account_id", OpenApiTypes.UUID, OpenApiParameter.PATH)
            ],
            summary="Altera parcialmente informações do usuário, apenas o proprio usuário pode fazer alteração na sua conta",
            description="Rota permite fazer uma alteração em um usuário através do ID passado pelo parâmetro 'account_id'",
            tags=["Rotas de Accounts"]
    )
    def patch(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @extend_schema(
            operation_id="accounts_delete",
            responses={200: AccountSerializer},
            parameters=[
                AccountSerializer,
                OpenApiParameter("account_id", OpenApiTypes.UUID, OpenApiParameter.PATH)
            ],
            summary="Deleta um usuário, apenas o proprio usuário pode fazer alteração na sua conta",
            description="Rota permite deletar um usuário através do ID passado pelo parâmetro 'account_id'",
            tags=["Rotas de Accounts"]
    )
    def delete(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)