from decimal import Decimal

from src.orders.domain.value_objects.item_quantity import ItemQuantity
from src.orders.domain.value_objects.order_item_id import OrderItemId
from src.orders.domain.value_objects.product_id import ProductId
from src.orders.domain.value_objects.product_name import ProductName
from src.orders.domain.value_objects.product_price import ProductPrice
from src.orders.domain.value_objects.total_amount import TotalAmount


class OrderItem:
  def __init__(
    self,
    order_item_id: OrderItemId,
    product_id: ProductId,
    product_name: ProductName,
    product_sku: str,
    product_image_url: str,
    quantity: ItemQuantity,
    unit_price: ProductPrice,
    discount_amount: Decimal = Decimal("0"),
    tax_amount: Decimal = Decimal("0"),
    notes: str | None = None,
  ):
    self._order_item_id = order_item_id
    self._product_id = product_id
    self._product_name = product_name
    self._product_sku = product_sku
    self._product_image_url = product_image_url
    self._quantity = quantity
    self._unit_price = unit_price
    self._discount_amount = discount_amount
    self._tax_amount = tax_amount
    self._notes = notes

  @property
  def order_item_id(self) -> OrderItemId:
    return self._order_item_id

  @property
  def product_id(self) -> ProductId:
    return self._product_id

  @property
  def product_name(self) -> ProductName:
    return self._product_name

  @property
  def product_sku(self) -> str:
    return self._product_sku

  @property
  def product_image_url(self) -> str:
    return self._product_image_url

  @property
  def quantity(self) -> ItemQuantity:
    return self._quantity

  @property
  def unit_price(self) -> ProductPrice:
    return self._unit_price

  @property
  def subtotal(self) -> TotalAmount:
    return TotalAmount(self.unit_price.value * Decimal(self.quantity.value))

  @property
  def discount_amount(self) -> Decimal:
    return self._discount_amount

  @property
  def tax_amount(self) -> Decimal:
    return self._tax_amount

  @property
  def total(self) -> TotalAmount:
    return TotalAmount((self.subtotal.value - self.discount_amount) + self.tax_amount)

  @property
  def notes(self) -> str | None:
    return self._notes

  def to_primitives(self) -> dict:
    return {
      "order_item_id": self._order_item_id.value,
      "product_id": self._product_id.value,
      "product_name": self._product_name.value,
      "product_sku": self._product_sku,
      "product_image_url": self._product_image_url,
      "quantity": self._quantity.value,
      "unit_price": float(self._unit_price.amount),
      "currency": self._unit_price.currency,
      "subtotal": float(self.subtotal.amount),
      "discount_amount": float(self._discount_amount),
      "tax_amount": float(self._tax_amount),
      "total": float(self.total.amount),
      "notes": self._notes,
    }

  def __eq__(self, other):
    if not isinstance(other, OrderItem):
      return False
    return self._order_item_id.value == other._order_item_id.value

  def __hash__(self):
    return hash(self._order_item_id.value)
