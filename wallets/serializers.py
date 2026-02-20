from decimal import Decimal

from rest_framework import serializers

from .models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    """Serializador para Wallet con todos los campos y validación de balance no negativo."""

    class Meta:
        model = Wallet
        fields = (
            "id",
            "user",
            "balance",
            "currency",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("user", "created_at", "updated_at")

    def validate_balance(self, value):
        if value is not None and value < Decimal("0"):
            raise serializers.ValidationError(
                "El balance no puede ser negativo."
            )
        return value
