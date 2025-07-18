from django.core.validators import MinValueValidator
from django.db.models import (
  CharField,
  DateTimeField,
  DecimalField,
  GenericIPAddressField,
  Index,
  PositiveIntegerField,
  TextChoices,
  TextField,
  UUIDField,
)
from django.utils.timezone import now

from src.shared.infrastructure.persistences.base_models import BaseDAO


class OrderDAO(BaseDAO):
  """
  total_amount: Total amount before discounts
  total_discount: Sum of all discounts
  tax_amount: Calculated taxes
  final_amount: Amount to be paid after discounts and taxes
  paid_amount: Sum of all payments received
  balance_due: Outstanding balance (final_amount - paid_amount)
  """

  class Source(TextChoices):
    WEB = "web", "Web"
    MOVIL = "movil", "Móvil"

  class Status(TextChoices):
    DRAFT = "draft", "Borrador"
    PENDING_PAYMENT = "pending_payment", "Pago Pendiente"
    PARTIALLY_PAID = "partially_paid", "Pago Parcial"
    PAID = "paid", "Pagado"
    SHIPPED = "shipped", "Enviado"
    DELIVERED = "delivered", "Entregado"
    CANCELLED = "cancelled", "Cancelado"
    REFUNDED = "refunded", "Reembolsado"

  order_date = DateTimeField(default=now)
  order_number = CharField(max_length=100, unique=True)
  customer_id = UUIDField(null=True, blank=True)
  customer_name = CharField(max_length=160, null=True, blank=True)
  seller_id = UUIDField(null=True, blank=True)
  seller_name = CharField(max_length=160, null=True, blank=True)
  ip_address = GenericIPAddressField()
  source = CharField(max_length=20, choices=Source.choices)
  status = CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
  total_items = PositiveIntegerField()
  currency = CharField(max_length=3)
  amount = DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
  discount = DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
  tax_amount = DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
  total_amount = DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
  paid_amount = DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
  balance_due = DecimalField(max_digits=12, decimal_places=2, default=0)
  notes = TextField(blank=True, null=True)

  class Meta:
    db_table = "orders"
    verbose_name = "Order"
    verbose_name_plural = "Orders"
    ordering = ["-order_date"]
    indexes = [
      Index(fields=["order_number"]),
      Index(fields=["customer_id"]),
      Index(fields=["status"]),
      Index(fields=["created_at"]),
    ]

  def __str__(self):
    return f"Order #{self.order_number} - {self.get_status_display()}"
