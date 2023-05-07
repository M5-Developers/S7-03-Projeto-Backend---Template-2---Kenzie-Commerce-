from rest_framework import serializers
from rest_framework.views import Response, status

from address.models import Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["id", "street", "cep", "number"]
        extra_kwargs = {
            "id": {"read_only": True},
            "account_id": {"read_only": True}
        }

    def create(self, data):
        return Address.objects.create(**data)