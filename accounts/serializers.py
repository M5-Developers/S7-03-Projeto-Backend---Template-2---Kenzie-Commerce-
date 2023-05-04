from rest_framework import serializers
from .models import Account


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
            "email",
            "username",
            "password",
            "is_superuser",
            "is_staff"
        ]

        extra_kwargs = {"password": {"write_only": True}}