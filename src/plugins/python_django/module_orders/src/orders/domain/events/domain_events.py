from dataclasses import dataclass
from datetime import datetime


@dataclass
class OrderCreated:
  order_id: str
  customer_id: str
  total_amount: float
  currency: str
  occurred_on: datetime = datetime.now()


@dataclass
class OrderItemAdded:
  order_id: str
  order_item_id: str
  product_id: str
  quantity: int
  unit_price: float
  occurred_on: datetime = datetime.now()


@dataclass
class OrderItemRemoved:
  order_id: str
  order_item_id: str
  occurred_on: datetime = datetime.now()


@dataclass
class PaymentReceived:
  order_id: str
  payment_id: str
  amount: float
  currency: str
  occurred_on: datetime = datetime.now()


@dataclass
class OrderStatusChanged:
  order_id: str
  old_status: str
  new_status: str
  occurred_on: datetime = datetime.now()
