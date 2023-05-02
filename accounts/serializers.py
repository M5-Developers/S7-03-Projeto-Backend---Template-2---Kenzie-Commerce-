from rest_framework import serializers
from .models import Account

"""
    ModelSerializer:
        - Já vem com o .create e o .update nativos (sua versão mais genêrica).
            - Model.objects.create(**validated_data)
        - Mapeia os campos sem precisar descreve-los por completo
"""



class AccountSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(max_length=128, write_only=True)
    def create(self, validated_data: dict) -> Account:
        return Account.objects.create_user(**validated_data)

    class Meta:
        model = Account
        fields = [
            "id",
            "first_name",
            "last_name",
            "type",
            "email",
            "username",
            "password",
        ]

        extra_kwargs = {"password": {"write_only": True}}