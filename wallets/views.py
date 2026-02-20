from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Wallet
from .serializers import WalletSerializer


class WalletViewSet(ModelViewSet):
    """ViewSet para Wallet con acciones: balance, activate, deactivate."""

    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Wallet.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["get"], url_path="balance")
    def balance(self, request, pk=None):
        """Consulta el balance de la wallet."""
        wallet = self.get_object()
        return Response(
            {
                "wallet_id": wallet.pk,
                "balance": str(wallet.balance),
                "currency": wallet.currency,
            }
        )

    @action(detail=True, methods=["post"], url_path="activate")
    def activate(self, request, pk=None):
        """Activa la wallet (is_active=True)."""
        wallet = self.get_object()
        wallet.is_active = True
        wallet.save(update_fields=["is_active", "updated_at"])
        return Response(WalletSerializer(wallet).data)

    @action(detail=True, methods=["post"], url_path="deactivate")
    def deactivate(self, request, pk=None):
        """Desactiva la wallet (is_active=False)."""
        wallet = self.get_object()
        wallet.is_active = False
        wallet.save(update_fields=["is_active", "updated_at"])
        return Response(WalletSerializer(wallet).data)
