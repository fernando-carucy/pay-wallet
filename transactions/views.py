from decimal import Decimal

from django.db import transaction as db_transaction
from django.db.models import F, Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from wallets.models import Wallet

from .models import Transaction, Transfer
from .serializers import TransactionSerializer, TransferSerializer


class TransactionViewSet(ModelViewSet):
    """ViewSet para Transaction. Al crear, procesa depósito/retiro y actualiza el balance de la wallet."""

    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(wallet__user=self.request.user)

    def perform_create(self, serializer):
        wallet = serializer.validated_data["wallet"]
        if wallet.user_id != self.request.user.pk:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Solo puedes crear transacciones en tus propias wallets.")

        amount = serializer.validated_data["amount"]
        transaction_type = serializer.validated_data["transaction_type"]
        with db_transaction.atomic():
            obj = serializer.save(status=Transaction.Status.PENDING)
            if transaction_type == Transaction.TransactionType.DEPOSIT:
                Wallet.objects.filter(pk=wallet.pk).update(
                    balance=F("balance") + amount
                )
            else:  # WITHDRAWAL (validación de balance ya hecha en el serializer)
                Wallet.objects.filter(pk=wallet.pk).update(
                    balance=F("balance") - amount
                )
            obj.status = Transaction.Status.COMPLETED
            obj.save(update_fields=["status", "updated_at"])


class TransferViewSet(ModelViewSet):
    """ViewSet para Transfer. Al crear, procesa la transferencia entre wallets (resta origen, suma destino)."""

    serializer_class = TransferSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transfer.objects.filter(
            Q(from_wallet__user=self.request.user)
            | Q(to_wallet__user=self.request.user)
        )

    def perform_create(self, serializer):
        from_wallet = serializer.validated_data["from_wallet"]
        if from_wallet.user_id != self.request.user.pk:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Solo puedes enviar desde tus propias wallets.")

        to_wallet = serializer.validated_data["to_wallet"]
        amount = serializer.validated_data["amount"]

        with db_transaction.atomic():
            obj = serializer.save(status=Transfer.Status.PENDING)
            Wallet.objects.filter(pk=from_wallet.pk).update(
                balance=F("balance") - amount
            )
            Wallet.objects.filter(pk=to_wallet.pk).update(
                balance=F("balance") + amount
            )
            obj.status = Transfer.Status.COMPLETED
            obj.save(update_fields=["status", "updated_at"])
