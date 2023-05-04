from accounts.permissions import IsAccountOnwer
from .serializers import AccountSerializer
from .models import Account
from rest_framework import generics

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from carts.models import Cart

# MRO - Method Resolution Order
class AccountView(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def perform_create(self, serializer):
        serializer.save()
        cart = Cart.objects.create(account_id=serializer.data['id'])

    @extend_schema(
        operation_id="accounts_list",
        responses={200: AccountSerializer},
        description="Rota de listagem de contas de usuários",
        summary="Sumário Listagem de Contas de usuário",
        tags=["Tag Listagem de Contas de usuários"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class AccountDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountOnwer]

    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    lookup_url_kwarg = "account_id"
