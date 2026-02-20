from decimal import Decimal

from django.db import models
from django.conf import settings


class Wallet(models.Model):
    class Currency(models.TextChoices):
        USD = "USD", "USD"
        EUR = "EUR", "EUR"
        GBP = "GBP", "GBP"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wallets",
    )
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    currency = models.CharField(
        max_length=3,
        choices=Currency.choices,
        default=Currency.USD,
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "wallet"
        verbose_name_plural = "wallets"

    def __str__(self):
        return f"{self.user.email} - {self.get_currency_display()} ({self.balance})"

    def update_balance(self, amount):
        """Actualiza el balance de la wallet y guarda los cambios."""
        self.balance = amount
        self.save(update_fields=["balance", "updated_at"])
