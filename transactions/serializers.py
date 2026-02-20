from decimal import Decimal

from rest_framework import serializers

from .models import Transaction, Transfer


class TransactionSerializer(serializers.ModelSerializer):
    """Serializador para Transaction con validación de balance suficiente en retiros."""

    class Meta:
        model = Transaction
        fields = (
            "id",
            "wallet",
            "amount",
            "transaction_type",
            "status",
            "description",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")

    def validate_amount(self, value):
        if value is not None and value <= 0:
            raise serializers.ValidationError(
                "El monto debe ser mayor que cero."
            )
        return value

    def validate(self, attrs):
        wallet = attrs.get("wallet") or (self.instance.wallet if self.instance else None)
        amount = attrs.get("amount")
        transaction_type = attrs.get("transaction_type") or (
            self.instance.transaction_type if self.instance else None
        )

        if (
            wallet
            and amount is not None
            and transaction_type == Transaction.TransactionType.WITHDRAWAL
        ):
            if wallet.balance < amount:
                raise serializers.ValidationError(
                    {"amount": "Balance insuficiente en la wallet."}
                )
        return attrs


class TransferSerializer(serializers.ModelSerializer):
    """Serializador para Transfer con validación de balance suficiente y wallets distintas."""

    class Meta:
        model = Transfer
        fields = (
            "id",
            "from_wallet",
            "to_wallet",
            "amount",
            "status",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")

    def validate_amount(self, value):
        if value is not None and value <= 0:
            raise serializers.ValidationError(
                "El monto debe ser mayor que cero."
            )
        return value

    def validate(self, attrs):
        from_wallet = attrs.get("from_wallet") or (
            self.instance.from_wallet if self.instance else None
        )
        to_wallet = attrs.get("to_wallet") or (
            self.instance.to_wallet if self.instance else None
        )
        amount = attrs.get("amount")
        if amount is None and self.instance:
            amount = self.instance.amount

        if from_wallet and to_wallet and from_wallet.pk == to_wallet.pk:
            raise serializers.ValidationError(
                {"to_wallet": "No se puede transferir a la misma wallet."}
            )

        if from_wallet and amount is not None and amount > 0:
            if from_wallet.balance < amount:
                raise serializers.ValidationError(
                    {"amount": "Balance insuficiente en la wallet de origen."}
                )

        return attrs
