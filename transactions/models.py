from decimal import Decimal

from django.db import models
from django.core.exceptions import ValidationError

from wallets.models import Wallet


class Transaction(models.Model):
    """Depósitos y retiros sobre una wallet."""

    class TransactionType(models.TextChoices):
        DEPOSIT = "DEPOSIT", "Depósito"
        WITHDRAWAL = "WITHDRAWAL", "Retiro"

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pendiente"
        COMPLETED = "COMPLETED", "Completado"
        FAILED = "FAILED", "Fallido"

    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name="transactions",
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(
        max_length=10,
        choices=TransactionType.choices,
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
    )
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "transaction"
        verbose_name_plural = "transactions"

    def __str__(self):
        return f"{self.get_transaction_type_display()} {self.amount} - {self.wallet} ({self.get_status_display()})"

    def clean(self):
        if self.transaction_type == self.TransactionType.WITHDRAWAL and self.amount is not None:
            if self.amount <= 0:
                raise ValidationError({"amount": "El monto debe ser mayor que cero."})
            if self.pk is None:  # nueva transacción
                current_balance = self.wallet.balance if self.wallet_id else Decimal("0")
                if current_balance < self.amount:
                    raise ValidationError(
                        {"amount": "Balance insuficiente en la wallet."}
                    )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Transfer(models.Model):
    """Transferencias entre wallets."""

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pendiente"
        COMPLETED = "COMPLETED", "Completado"
        FAILED = "FAILED", "Fallido"

    from_wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name="transfers_sent",
    )
    to_wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name="transfers_received",
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "transfer"
        verbose_name_plural = "transfers"

    def __str__(self):
        return f"{self.amount} {self.from_wallet} → {self.to_wallet} ({self.get_status_display()})"

    def clean(self):
        if self.from_wallet_id and self.to_wallet_id:
            if self.from_wallet_id == self.to_wallet_id:
                raise ValidationError(
                    {"to_wallet": "No se puede transferir a la misma wallet."}
                )
        if self.amount is not None and self.amount <= 0:
            raise ValidationError({"amount": "El monto debe ser mayor que cero."})
        if (
            self.from_wallet_id
            and self.amount is not None
            and self.amount > 0
            and self.pk is None
        ):
            if self.from_wallet.balance < self.amount:
                raise ValidationError(
                    {"amount": "Balance insuficiente en la wallet de origen."}
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
