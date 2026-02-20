from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TransactionViewSet, TransferViewSet

router = DefaultRouter()
# Registrar "transfers" primero para que /transfers/ no sea capturado como pk de transactions
router.register(r"transfers", TransferViewSet, basename="transfer")
router.register(r"", TransactionViewSet, basename="transaction")

urlpatterns = [
    path("", include(router.urls)),
]
