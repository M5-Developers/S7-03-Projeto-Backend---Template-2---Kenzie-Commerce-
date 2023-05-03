from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import Response, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from address.models import Address
from address.serializers import AddressSerializer
from address.permissions import AdminOrOwnerPermission, IsAdmin

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

    def perform_create(self, serializer):
        find_address = Address.objects.filter(**serializer.validated_data)
        if find_address:
            return Response(
                { "message": "Endereço já registrado." },
                status.HTTP_409_CONFLICT
            )

        find_user = Account.objects.filter(id=self.request.user.id).first()
        serializer.save(account=find_user)

class AddressByIdView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AdminOrOwnerPermission]

    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    lookup_url_kwarg = "address_id"
