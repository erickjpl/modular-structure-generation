from dataclasses import dataclass
from datetime import datetime

from src.orders.domain.entities.order import Order
from src.orders.domain.entities.order_item import OrderItem
from src.shared.domain.queries.response import Response


@dataclass(frozen=True)
class OrderItemDTO:
  product_id: str
  product_name: str
  product_sku: str
  product_image_url: str
  quantity: int
  unit_price: float
  subtotal: float
  discount_amount: float
  tax_amount: float
  total: float
  notes: str = None

  @staticmethod
  def from_entity(item: OrderItem) -> "OrderItemDTO":
    return OrderItemDTO(
      product_id=str(item.product_id),
      product_name=item.product_name,
      product_sku=item.product_sku,
      product_image_url=item.product_image_url,
      quantity=item.quantity,
      unit_price=float(item.unit_price),
      subtotal=float(item.subtotal),
      discount_amount=float(item.discount_amount),
      tax_amount=float(item.tax_amount),
      total=float(item.total),
      notes=item.notes,
    )


@dataclass(frozen=True)
class OrderDTO(Response):
  id: str
  order_date: datetime
  order_number: str
  customer_id: str
  customer_name: str
  seller_id: str
  seller_name: str
  ip_address: str
  source: str
  status: str
  total_items: int
  currency: str
  amount: float
  discount: float
  tax_amount: float
  total_amount: float
  paid_amount: float
  balance_due: float
  notes: str = None
  items: list[OrderItemDTO] = None

  @staticmethod
  def from_entity(order: Order) -> "OrderDTO":
    return OrderDTO(
      id=str(order.id),
      order_date=order.order_date,
      order_number=order.order_number,
      customer_id=str(order.customer_id) if order.customer_id else None,
      customer_name=order.customer_name,
      seller_id=str(order.seller_id) if order.seller_id else None,
      seller_name=order.seller_name,
      ip_address=order.ip_address,
      source=order.source,
      status=order.status,
      total_items=order.total_items,
      currency=order.currency,
      amount=float(order.amount),
      discount=float(order.discount),
      tax_amount=float(order.tax_amount),
      total_amount=float(order.total_amount),
      paid_amount=float(order.paid_amount),
      balance_due=float(order.balance_due),
      notes=order.notes,
      items=[OrderItemDTO.from_entity(item) for item in order.items.all()] if hasattr(order, "items") else None,
    )
