from django.core.validators import MinValueValidator
from django.db.models import (
  CASCADE,
  CharField,
  DecimalField,
  ForeignKey,
  PositiveIntegerField,
  TextField,
  URLField,
  UUIDField,
)

from src.orders.infrastructure.persistences.models.order import OrderDAO
from src.shared.infrastructure.persistences.base_models import BaseDAO


class OrderItemDAO(BaseDAO):
  """
  unit_price: Unit price at the time of order
  subtotal: quantity * unit_price
  discount_amount: Discount applied to this item
  tax_amount: Taxes for this item
  total: Subtotal - discount + tax
  """

  order = ForeignKey(OrderDAO, related_name="items", on_delete=CASCADE)
  product_id = UUIDField()
  product_name = CharField(max_length=160)
  product_sku = CharField(max_length=75)
  product_image_url = URLField()
  quantity = PositiveIntegerField()
  unit_price = DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
  subtotal = DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
  discount_amount = DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
  tax_amount = DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
  total = DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
  notes = TextField(blank=True, null=True)

  class Meta:
    db_table = "order_items"
    verbose_name = "Order Item"
    verbose_name_plural = "Order Items"
    ordering = ["id"]

  def __str__(self):
    return f"Order Item {self.product_id} x {self.quantity}"
