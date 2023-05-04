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

    def post(self, request, *args, **kwargs):
        serialized = self.serializer_class(data=request.data)
        serialized.is_valid()
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
