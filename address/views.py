from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import Response, status
from rest_framework_simplejwt.authentication import JWTAuthentication

from address.models import Address
from address.serializers import AddressSerializer
from address.permissions import AdminOrOwnerPermission

from users.models import User

# Create your views here.
class AddressView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    def get_permissions(self):
        if self.request.method == "GET":
            return [AdminOrOwnerPermission]
        return super().get_permissions()

    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def perform_create(self, serializer):
        find_address = Address.objects.filter(**serializer)
        if find_address:
            return Response(
                { "message": "Endereço já registrado." },
                status.HTTP_409_CONFLICT
            )

        find_user = User.objects.filter(id=self.user.id).first()
        serializer.save(user=find_user)

class AddressByIdView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AdminOrOwnerPermission]

    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    lookup_url_kwarg = "address_id"
