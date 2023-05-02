from rest_framework import serializers

from address.models import Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        field = ["id", "street", "cep", "number", "user_id"]
        extra_kwargs = {
            "id": {"read_only": True},
            "user_id": {"read_only": True}
        }

    def create(self, data):
        return Address.objects.create(**data)