from dataclasses import dataclass
from typing import List

from src.shared.domain.commands.command import Command
from src.orders.domain.value_objects.order_id import OrderId
from src.orders.domain.value_objects.order_number import OrderNumber
from src.orders.domain.value_objects.customer_id import CustomerId
from src.orders.domain.value_objects.customer_name import CustomerName
from src.orders.domain.value_objects.seller_id import SellerId
from src.orders.domain.value_objects.seller_name import SellerName
from src.orders.domain.entities.order import OrderSource
from src.orders.domain.entities.order_item import OrderItem

@dataclass(frozen=True)
class CreateOrderCommand(Command):
  order_id: OrderId
  order_number: OrderNumber
  customer_id: CustomerId
  customer_name: CustomerName
  seller_id: SellerId
  seller_name: SellerName
  ip_address: str
  source: OrderSource
  currency: str
  items: List[OrderItem]
